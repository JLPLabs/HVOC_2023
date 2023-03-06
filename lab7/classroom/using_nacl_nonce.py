#
# reference:
# https://pynacl.readthedocs.io/en/latest/public/#nacl-public-box

import nacl.utils
from nacl.public import PrivateKey, Box

# notes on key naming
# P/Kx  -- Public/Private keypair for entity x
# Sx    -- Symmetric key for entity x

# Generate Bob's private key (!! keep this secret !!)
Kb = PrivateKey.generate()

# Use the private key to create the public key -- this must be shared
Pb = Kb.public_key

# Alice does the same thing
Ka = PrivateKey.generate()
Pa = Ka.public_key

# <here Alice and Bob exchange public keys>

# Bob wants to box some data for Alice;
# He needs his private key and Alice's public key
boxerBA = Box(Kb, Pa)

nonce = 1
nonceb = nonce.to_bytes(24, 'big')

data = bytes.fromhex("00000000 11111111 22222222 33333333")
print("data to secure")
print(data.hex(" ", 4))
print("using nonce")
print(nonceb.hex(" ", 4))

# the library could automatically created a nonce for us, but we choose to create our own.
# using boxerBA results in a box that is:
# mac || nonce || data   === 16 bytes || 24 bytes || len(data)
# so total length is 40 bytes longer than data
box = boxerBA.encrypt(data, nonceb)
print("size of box is 40 + len(data): %d" %(len(box)))

### Alice is given the box, 'box', and needs to open it.

# create a box opener, she uses Bob's public key and her private key
boxopenerBA = Box(Ka, Pb)

# use the opener
pt = boxopenerBA.decrypt(box)

print("data received by Alice")
print(pt.hex(" ", 4))
