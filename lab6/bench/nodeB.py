# send one message, the public key of this node
# catch one message, the public key of the other node
# create the key and print it
# asyncio: https://python-can.readthedocs.io/en/master/asyncio.html
# x25519: https://pynacl.readthedocs.io/en/latest/public/#nacl-public-box

import asyncio
import time

import can
from can.notifier import MessageRecipient

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# -----------------------------------------------------------------------------
# globals
bustype = 'socketcan'
PGN  = 0xCAFE
PRIO = 0x03
channel = 'vcan0'
sa      = 0x42
Kb = PrivateKey.generate()
Pb = Kb.public_key
sharedsecret = bytes.fromhex("00") 
sharedkey = bytes.fromhex("00") 

#------------------------------------------------------------------------------
# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  global sharedkey
  print("[nodeB] the shared key is: %s" % (sharedkey.hex(" ", 4)), flush=True)
  print("\ntext_ic caught SIGINT. Shutting down...\n")
  exit(1)
signal.signal(signal.SIGINT, handler)

# -----------------------------------------------------------------------------
# return arbitration id
def arbid(priority, pgn, sa):
  field1 = (priority << 2) << 24
  field2 = pgn << 8
  field3 = sa
  return field1 | field2 | field3 

# deconstruct arbitration ID; return priority, pgn, sa
def arbid_decode(arbid):
  sa = arbid & 0xFF
  arbid = arbid >> 8
  pgn = arbid & 0xFFFF
  priority = arbid >> 18
  return priority, pgn, sa

# given the other node's public key we can calculate:
# 1. The shared secret
# 2. The shared key (from the shared secret)
def readcanbus(msg):
    global Kb
    arbid = msg.arbitration_id
    data = msg.data
    priority, pgn, sa = arbid_decode(arbid)
    if pgn == 0xCAFE:
        Pa = bytes(data)
        boxerBA = Box(Kb, PublicKey(Pa))
        sharedsecret = boxerBA.shared_key()   # library docs make this sound
                                              # like a shared secret, despite
                                              # its name.
        # use a Key Derivation Function (KDF) to convert secret into an AES-128 key
        # (that means we need 16 bytes from the kdf)
        kdf = ...
        sharedkey = kdf(...)

        print("[nodeB] the shared key is: %s" % (sharedkey.hex(" ", 4)), flush=True)
    else:
        print("[nodeB] unexpected PGN received: [%x]\n" % (pgn))

# =============================================================================
async def main():

  with can.Bus(channel=channel, interface=bustype, fd=True) as bus:

      # get ready to send our public key
      canid = arbid(PRIO, PGN, sa)
  
      # x25521 keys are 32 bytes long
      data = bytes(Pb) 
      msg = can.Message(arbitration_id=canid, data=data, is_extended_id=True,
                        is_fd=True, dlc=32, check=True)

      # canbus listeners
      reader0 = can.AsyncBufferedReader()
      listeners0 = [
          reader0,        # AsyncBufferedReader() listener
          readcanbus,     # callback
      ]

      # create Notifier with an explicit loop to use for scheduling callbacks  	
      loop0 = asyncio.get_running_loop()
      notifier0 = can.Notifier(bus, listeners0, loop=loop0)

      # wait (in case other node needs time to be launched)
      for _ in range(10):
          print(".", end="")

          # send our public key
          bus.send(msg)

          await asyncio.sleep(1.0)

      # timeout
      print("timeout")


      # clean-up
      notifier0.stop()




if __name__ == "__main__":
  asyncio.run(main())
