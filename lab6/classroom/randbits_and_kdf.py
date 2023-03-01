from cryptography.hazmat.primitives import hashes                        # for SHA256 hash
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash   # for kdf
import secrets                                                           # for randbits

x = secrets.randbits(8)
print(x)

x = secrets.randbits(64)
xb = x.to_bytes(8, "big")        # converts 64 bits into 8 bytes
print(xb.hex(" ", 4))            # example: 61e015f7 920a8f0a

y = secrets.randbits(64)
yb = y.to_bytes(8, "big")        # example: 13a56ccd bed1a7c8

zb = xb + yb
print(zb.hex(" ", 4))            # example: 61e015f7 920a8f0a 13a56ccd bed1a7c8

Sn = bytes.fromhex("00000000 11111111 22222222 33333333")

keymaterial = Sn + zb
print(keymaterial.hex(" ", 4))   # example: 00000000 11111111 22222222 33333333 61e015f7 920a8f0a 13a56ccd bed1a7c8

sv = kdf.derive(keymaterial)
print(sv.hex(" ", 4))            # example: fb2e494f df1c65a1 01e8649f f59f7bd6
