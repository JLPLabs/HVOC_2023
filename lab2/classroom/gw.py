#!/usr/bin/python3
# source: https://python-can.readthedocs.io/en/master/asyncio.html
#   hereafter, [rtd] = source url through "master/"

"""
This example demonstrates how to use async IO with python-can.

This is a bi-directional gateway.
"""
import math
import sys, getopt

import asyncio
from typing import List

import can
from can.notifier import MessageRecipient

#------------------------------------------------------------------------------
# globals
bustype = 'socketcan'
bus0 = ''              # bus0 connection (for port0)
bus1 = ''              # bus1 connection (for port1)
f = ''                 # file handle for log file

# globals set by command line arguments (w/ default, if any)
port0 = 'vcan0'
port1 = 'vcan1'
filename = ''
verbose = False
dolog = False        # true when we should write to file

usage = """
-0  --port0  <bus_name>    set bus connected to port 0
-1  --port1  <bus_name>    set bus connected to port 1
-o  --out    <file_name>   save a copy of the forwarded data in a log file
-v                         verbose output to show port values being used

if -o / --out is not specified then no file is created.

default: --port0 {0} --port1 {1} 
""".format(port0, port1)

#------------------------------------------------------------------------------
# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  global dolog, f
  if dolog:
    f.close()
  exit(1)
signal.signal(signal.SIGINT, handler)

# convert speed to j1939 2 bytes
# usage: byte1, bytes2 = speed2j1939(20)
#        data = [byte1, byte2, ...remaining 6 bytes...]
def speed2j1939(mph):
    # convert mph to meter/sec
    mps = mph / 2.23694
 
    # convert m/s to bytes
    byte2 = math.floor(mps/0.256)
    byte1 = math.floor((mps-byte2*0.256)/0.001)
   
    return byte1, byte2

# convert FE49 to mph   [ground speed]
def pgnFE49(data):
    b1 = data[0]
    b2 = data[1]
    mps = b2 * 0.256 + b1 * 0.001
    mph = mps * 2.23694
    return b1, b2, mph
  
def doublespeed(msg: can.Message) -> can.Message:
    canid = msg.arbitration_id
    pgn = (canid >> 8) & 0xffff
    if pgn == 0xFE49: 
       b1, b2, speed = pgnFE49(msg.data)
       speed = speed * 2
       b1, b2  = speed2j1939(speed)
       msg.data[0] = b1
       msg.data[1] = b2
       return msg     # return msg with doubled ground speed
    else:
       return msg     # msg wasn't ground speed, so return it unchanged

def print_message(msg: can.Message) -> None:
    print(msg)

def write_message(msg: can.Message) -> None:
    global dolog, f
    if dolog:
      f.write(msg.__str__())
      f.write("\n")

def fwd_0to1(msg: can.Message) -> None:
    global bus1
    msg = doublespeed(msg)
    bus1.send(msg)
    write_message(msg)

def fwd_1to0(msg: can.Message) -> None:
    global bus0
    msg = doublespeed(msg)
    bus0.send(msg)
    write_message(msg)


# handle command line args
def set_globals(argv):
  global port0, port1, verbose, filename, dolog
  try:
    opts, args = getopt.getopt(argv, "hv0:1:o:",["port0=","port1=","out="])
  except getopt.GetoptError as err:
    print(err)
    print(usage)
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-h":
      print(usage)
      sys.exit()
    elif opt == "-v":
      verbose = True
    elif opt in ("-0", "--port0"):
      port0 = arg
    elif opt in ("-1", "--port1"):
      port1 = arg
    elif opt in ("-o", "--out"):
      dolog = True
      filename = arg

  if verbose:
    print("   port0: %s" % (port0))
    print("   port1: %s" % (port1))
    print("filename: %s" % (filename))
    print(" logging: %s" % (dolog))


# =============================================================================
async def main() -> None:
    """The main function that runs in the loop."""
    global bus0, bus1, dolog, f

    bus0 = can.Bus(interface="socketcan", channel=port0) 
    bus1 = can.Bus(interface="socketcan", channel=port1)

    if dolog:
      f = open(filename, "w")

    # port1 listeners ..............................................
    reader1 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners1: List[MessageRecipient] = [
        reader1,        # AsyncBufferedReader() listener
        fwd_1to0,       # Callback function
    ]

    # port0 listeners ..............................................
    reader0 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners0: List[MessageRecipient] = [
        reader0,        # AsyncBufferedReader() listener
        fwd_0to1,       # Callback function
    ]
    
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    #   notifier is used as a message distributor for a bus. Notifier
    #   creates a thread to read messages from the bus and distributes
    #   them to listeners. [rtd]/api.html#notifier
    loop1 = asyncio.get_running_loop()
    notifier1 = can.Notifier(bus1, listeners1, loop=loop1)
    loop0 = asyncio.get_running_loop()
    notifier0 = can.Notifier(bus0, listeners0, loop=loop0)

    print("forwarding between %s and %s" %(port0, port1))
    print(" ")
    print("use 'cansniffer' on either or both vcan networks to watch traffic")
    print("..........")
    print("^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg1 = await reader1.get_message()
        msg0 = await reader0.get_message()

    # Clean-up
    notifier0.stop()
    notifier1.stop()


if __name__ == "__main__":
    set_globals(sys.argv[1:])
    asyncio.run(main())
