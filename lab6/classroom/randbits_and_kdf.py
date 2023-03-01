from cryptography.hazmat.primitives import hashes                        # for SHA256 hash
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash   # for kdf
import secrets                                                           # for randbits

# x and y will be entropy ('nonces' in this case)

x = secrets.randbits(8)
print(x)

x = secrets.randbits(64)
xb = x.to_bytes(8, "big")        # converts 64 bits into 8 bytes
print(xb.hex(" ", 4))            # example: 61e015f7 920a8f0a

y = secrets.randbits(64)
yb = y.to_bytes(8, "big")        # example: 13a56ccd bed1a7c8

# z is the conatenation of all nonces
zb = xb + yb
print(zb.hex(" ", 4))            # example: 61e015f7 920a8f0a 13a56ccd bed1a7c8

# Sn is the long-lived base key
Sn = bytes.fromhex("00000000 11111111 22222222 33333333")

# combine base with nonces (order matters! all participants mush use the same order)
keymaterial = Sn + zb
print(keymaterial.hex(" ", 4))   # example: 00000000 11111111 22222222 33333333 61e015f7 920a8f0a 13a56ccd bed1a7c8

# use the key material to create a new key, Sv
kdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=16, otherinfo=b"00000000")
Sv = kdf.derive(keymaterial)

print(Sv.hex(" ", 4))            # example: fb2e494f df1c65a1 01e8649f f59f7bd6
