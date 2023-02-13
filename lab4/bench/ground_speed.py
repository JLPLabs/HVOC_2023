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
PGN  = 0xFE49   # 0xFE >= 0xF0, therefore "broadcast"; 0xFE49 is ground speed
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
  speed = 0     # mph
  direction = 1
  
  while True:
    # our speed is ramping up and down, forever, 0..42 mph
    speed = speed + direction * 1
    if speed > 42:
      direction = -1
      speed = 42
    if speed < 0:
      direction = 1
      speed = 0
  
    byte1, byte2 = speed2j1939(speed)
    data = [byte1, byte2, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # 0x02F3 = 1.689 mph
    msg = can.Message(arbitration_id=canid, data=data, is_extended_id=True, check=True)

    msg = adapter(msg)

    # the secure data is 8 bytes long
    msg = can.Message(arbitration_id=canid, data=msg.data, is_extended_id=True, is_fd=True, dlc=8, check=True)
    bus.send(msg)
    time.sleep(1) 

if __name__ == "__main__":
  set_globals(sys.argv[1:])
  main()
