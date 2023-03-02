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
PGN  = 0xFE43   # 0xFE >= 0xF0, therefore "broadcast"; 0xFE43 is pto speed
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

# convert pto rpm to j1939 2 bytes
# usage: byte1, bytes2 = pto2j1939(1200)
#        data = [byte1, byte2, ...remaining 6 bytes...]
def pto2j1939(rpm):
  # convert rpm to bits
  bits = math.floor(rpm / 0.125)
  
  # convert m/s to bytes
  byte1 = bits & 0xff
  byte2 = (bits >> 8) & 0xff

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
  speed = 0     # rpm
  direction = 1
  
  while True:
    # our speed is ramping up and down, forever, 0..2000 rpm
    speed = speed + direction * 100
    if speed > 2000:
      direction = -1
      speed = 2000
    if speed < 0:
      direction = 1
      speed = 0
  
    byte1, byte2 = pto2j1939(speed)
    data = [byte1, byte2, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  
    msg = can.Message(arbitration_id=canid, data=data, is_extended_id=True, check=True)

    msg = adapter(msg)

    # the secure data is 48 bytes long
    msg = can.Message(arbitration_id=canid, data=msg.data, is_extended_id=True, is_fd=True, dlc=48, check=True)
    bus.send(msg)
    time.sleep(1) 

if __name__ == "__main__":
  set_globals(sys.argv[1:])
  main()
