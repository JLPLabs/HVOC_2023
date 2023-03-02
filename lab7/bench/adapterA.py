# adapter A
#
# reference:
# https://pynacl.readthedocs.io/en/latest/public/#nacl-public-box

# msg = [   box    ]
# len(box) = lent(pt) + 40

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# need to read keys from disk 
# (this is a simplification for our lab; DO NOT DO THIS IN PRODUCTION)
pb_name = "Pb.key"
ka_name = "Ka.key"

with open(pb_name, "rb") as key_file:
   Pb = key_file.read()

with open(ka_name, "rb") as key_file:
   Ka = key_file.read()

boxopenerBA = Box(PrivateKey(Ka), PublicKey(Pb))

def adapter(msg):
   global boxerpenerBA

   return msg
