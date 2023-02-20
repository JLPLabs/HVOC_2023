#
# reference:
# https://pynacl.readthedocs.io/en/latest/public/#nacl.public.Box
# https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#concatkdf 

import nacl.utils
from nacl.public import PrivateKey, Box

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash

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

# By sharing just their public keys with each other,
# Alice and Bob have enough to derive a shared secret

# Alice knows her private key and Bob's public key
boxerAB = Box(Ka, Pb)
sharedsecret = boxerAB.shared_key()   # CONFUSING... the library docs say
                                   # we are getting both the shared secret and a key.
                                   # We are going to assume it is just the shared secret
                                   # and that we still need to generate the key.

# since we want an AES-128 key we still need to do a KDF and get 16 bytes
ckdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=16, otherinfo=b"00000000")
sharedkey = ckdf.derive(sharedsecret)

print("[Alice] the shared key is: %s" % (sharedkey.hex(" ", 4)), flush=True)

# Bob knows his private key and Alices's public key
boxerBA = Box(Kb, Pa)
sharedsecret = boxerBA.shared_key()
# since we want an AES-128 key we still need to do a KDF and get 16 bytes
ckdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=16, otherinfo=b"00000000")
sharedkey = ckdf.derive(sharedsecret)

print("  [Bob] the shared key is: %s" % (sharedkey.hex(" ", 4)), flush=True)

