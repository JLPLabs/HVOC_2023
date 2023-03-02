# adapter B
#
# reference:
# https://pynacl.readthedocs.io/en/latest/public/#nacl-public-box

# msg = [   box    ]
# len(box) = lent(pt) + 40

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

# need to read keys from disk 
# (this is a simplification for our lab; DO NOT DO THIS IN PRODUCTION)
pa_name = "Pa.key"
kb_name = "Kb.key"

with open(pa_name, "rb") as key_file:
   Pa = key_file.read()

with open(kb_name, "rb") as key_file:
   Kb = key_file.read()

boxerBA = Box(PrivateKey(Kb), PublicKey(Pa))

def adapter(msg):
   global boxerBA

   return msg
