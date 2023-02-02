#!/usr/bin/python3
# source: https://python-can.readthedocs.io/en/master/asyncio.html
#   hereafter, [rtd] = source url through "master/"

"""
This example demonstrates how to use async IO with python-can.

This is a bi-directional gateway.
"""
import sys, getopt

import asyncio
from typing import List

import can
from can.notifier import MessageRecipient

#------------------------------------------------------------------------------
# globals
bustype = 'socketcan'
bus0 = ''
bus1 = ''

# globals set by command line arguments (w/ default, if any)
port0 = 'vcan0'
port1 = 'vcan1'
verbose = False

usage = """
-0  --port0  <bus_name>    set bus connected to port 0
-1  --port1  <bus_name>    set bus connected to port 1
-v                         verbose output to show port values being used

default: -0 {0} -1 {1}
""".format(port0, port1)

#------------------------------------------------------------------------------
# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  exit(1)
signal.signal(signal.SIGINT, handler)

def print_message(msg: can.Message) -> None:
    print(msg)

def fwd_0to1(msg: can.Message) -> None:
    global bus1
    bus1.send(msg)

def fwd_1to0(msg: can.Message) -> None:
    global bus0
    bus0.send(msg)


# handle command line args
def set_globals(argv):
  global channel, verbose
  try:
    opts, args = getopt.getopt(argv, "hv0:1:",["port0=","port1="])
  except getopt.GetoptError:
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

  if verbose:
    print("bus: %s" % (channel))


# =============================================================================
async def main() -> None:
    """The main function that runs in the loop."""
    global bus0, bus1

    bus0 = can.Bus(interface="socketcan", channel=port0) 
    bus1 = can.Bus(interface="socketcan", channel=port1)

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

    print("forwarding between %s to %s" %(port0, port1))
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
