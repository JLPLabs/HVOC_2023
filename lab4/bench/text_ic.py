#!/usr/bin/python3
# source: https://python-can.readthedocs.io/en/master/asyncio.html
#   hereafter, [rtd] = source url through "master/"

"""
Using async IO with python-can to read a few interesting j1939 messages:
   * ground speed (PGN FE49)
   * engine speed (PGN F004)
   * pto speed    (PGN FE43).

And convert them to engineering units at write them to the command line.
"""
import sys, getopt

import asyncio
from typing import List

import can
from can.notifier import MessageRecipient

# the security adapter is used to validate and/or decrypt secured messages
from adapterA import adapter

#------------------------------------------------------------------------------
# globals
bustype = 'socketcan'
mph     = 0     # ground speed, mph
erpm    = 0     # engine speed, rpm
prpm    = 0     # pto speed, rpm

# globals set by command line arguments (w/ default, if any)
channel = 'vcan0'
verbose = False

usage = """
-b  --bus   <bus_name> 
-v          verbose output to show -b value being used

default: -b {0}
""".format(channel)

#------------------------------------------------------------------------------
# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  print("\ntext_ic caught SIGINT. Shutting down...\n")
  exit(1)
signal.signal(signal.SIGINT, handler)

# -------------------------------------------------------
# deconstruct arbitration ID
# return priority, pgn, sa
def arbid_decode(arbid):
  sa = arbid & 0xFF
  arbid = arbid >> 8
  pgn = arbid & 0xFFFF
  priority = arbid >> 18
  return priority, pgn, sa

# convert FE49 to mph  [ground speed]
def pgnFE49(data):
  b1 = data[0]
  b2 = data[1]
  mps = b2 * 0.256 + b1 * 0.001
  mph = mps * 2.23694
  return b1, b2, mph

# convert F004 to rpm  [engine speed]
def pgnF004(data):
  b4 = data[3]
  b5 = data[4]
  bits = (b5 << 8) | b4 
  rpm = bits * 0.125
  return b4, b5, rpm

# convert FE43 to rpm  [engine speed]
def pgnFE43(data):
  b1 = data[0]
  b2 = data[1]
  bits = (b2 << 8) | b1 
  rpm = bits * 0.125
  return b1, b2, rpm


def readcanbus(msg: can.Message) -> None:
    msg = adapter(msg)   # pass the raw received message through security
    global mph, erpm, prpm
    """Regular callback function. Can also be a coroutine."""
    arbid = msg.arbitration_id
    data = msg.data
    priority, pgn, sa = arbid_decode(arbid)
    if pgn == 0xfe49:
       b1, b2, mph = pgnFE49(data)
    if pgn == 0xf004:
       b4, b5, erpm = pgnF004(data)
    if pgn == 0xfe43:
       b1, b2, prpm = pgnFE43(data)

    #print("vcan0: %d, %x, %x : %x %x" %(priority, pgn, sa, b1, b2), end="\r")
    print("[%s] | " %(channel), end="")
    print("ground speed: %4.1f | " %(mph), end="")
    print("engine speed: %4.0f | " %(erpm), end="")
    print("pto speed: %4.0f | " %(prpm), end="\r")


# handle command line args
def set_globals(argv):
  global channel, verbose
  try:
    opts, args = getopt.getopt(argv, "hvb:",["bus="])
  except getopt.GetoptError:
    print(usage)
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-h":
      print(usage)
      sys.exit()
    elif opt == "-v":
      verbose = True
    elif opt in ("-b", "--bus"):
      channel = arg

  if verbose:
    print("bus: %s" % (channel))


# =============================================================================
async def main() -> None:
    """The main function that runs in the loop."""

    canbus = can.Bus(interface=bustype, channel=channel, fd=True) 

    # canbus listeners ..............................................
    reader0 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners0: List[MessageRecipient] = [
        reader0,          # AsyncBufferedReader() listener
        readcanbus,       # Callback function
    ]
    
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    #   notifier is used as a message distributor for a bus. Notifier
    #   creates a thread to read messages from the bus and distributes
    #   them to listeners. [rtd]/api.html#notifier
    loop0 = asyncio.get_running_loop()
    notifier0 = can.Notifier(canbus, listeners0, loop=loop0)

    print("reading a few special J1939 messages from %s" % (channel))
    print(" ")
    print("use 'cansniffer' on %s to watch all traffic" %(channel))
    print("..........")
    print("^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg0 = await reader0.get_message()

    # Clean-up
    notifier0.stop()


if __name__ == "__main__":
    set_globals(sys.argv[1:])
    asyncio.run(main())
