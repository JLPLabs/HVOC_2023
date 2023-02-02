# 1 Hz message sent on J1939
import can
import math
import time
import sys, getopt

# the security adapter is used to secure outgoing messages
from adapterB import adapter

# -----------------------------------------------------------------------------
# globals
bustype = 'socketcan'
PGN  = 0xF004   # 0xFE >= 0xF0, therefore "broadcast"; 0xF004 is engine speed
PRIO = 0x03

# globals set by command line arguments (w/ default, if any)
channel = 'vcan0'
sa      = 0x40
verbose = False

usage = """
-b  --bus   <bus_name> 
-s  --sa    <source_address> can be decimal or hex
-v          verbose output to show -b and -s values being used

default: -b {0} -s {1:x} 
""".format(channel, sa)

# -----------------------------------------------------------------------------
# return arbitration id
def arbid(priority, pgn, sa):
  field1 = (priority << 2) << 24
  field2 = pgn << 8
  field3 = sa
  return field1 | field2 | field3 

# convert engine to j1939 2 bytes
# usage: byte4, bytes5 = engine2j1939(2060)
#        data = [...., byte4, byte5, ...remaining 3 bytes...]
def engine2j1939(rpm):
  # convert rpm to bits
  bits = math.floor(rpm / 0.125)
  
  # convert m/s to bytes
  byte4 = bits & 0xff
  byte5 = (bits >> 8) & 0xff

  return byte4, byte5

# handle command line args
def set_globals(argv):
  global channel, sa, verbose
  try:
    opts, args = getopt.getopt(argv, "hvb:s:",["bus=","sa="])
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
    elif opt in ("-s", "--sa"):
      if arg.isdecimal():
        sa = int(arg)
      else:
        sa = int(arg, 16)

  if verbose:
    print("bus: %s" % (channel))
    print(" sa: %#x (%d)" % (sa, sa))


# =============================================================================
def main():
  bus = can.Bus(channel=channel, interface=bustype, fd=True)
  canid = arbid(PRIO, PGN, sa)
  speed = 0     # rpm
  direction = 1
  
  while True:
    # our speed is ramping up and down, forever, 0..4800 rpm
    speed = speed + direction * 25
    if speed > 4800:
      direction = -1
      speed = 4800
    if speed < 0:
      direction = 1
      speed = 0
  
    byte4, byte5 = engine2j1939(speed)
    data = [0xFF, 0xFF, 0xFF, byte4, byte5, 0xFF, 0xFF, 0xFF]  
    msg = can.Message(arbitration_id=canid, data=data, is_extended_id=True, check=True)

    msg = adapter(msg)

    # the secure data is 8 bytes long
    msg = can.Message(arbitration_id=canid, data=msg.data, is_extended_id=True, is_fd=True, dlc=8, check=True)
    bus.send(msg)
    time.sleep(1) 

if __name__ == "__main__":
  set_globals(sys.argv[1:])
  main()
