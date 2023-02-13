#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/mac/cmac/

from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

Sx = bytes.fromhex("00000000 11111111 22222222 33333333")
c  = cmac.CMAC(algorithms.AES(Sx))

data = bytes.fromhex("00 11 22 33 44 55 66")
c.update(data)
tag = c.finalize()
print("tag - has length %d" % (len(tag)))
print(tag.hex(" ", 4))
tagprime = tag[0]
print("tagprime")
print("%02x" % (tagprime))


data2 = bytes.fromhex("01 11 22 33 44 55 66")
c2 = cmac.CMAC(algorithms.AES(Sx))
c2.update(data2)
tag2 = c2.finalize()
print("\n\nonly one bit difference in data...")
print("see the new CMAC value, tag2:")
print(tag2.hex(" ", 4))

