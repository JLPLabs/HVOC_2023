#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/mac/cmac/

from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

Sx = bytes.fromhex("00000000 11111111 22222222 33333333")

count = 41

c  = cmac.CMAC(algorithms.AES(Sx))
data = int.to_bytes(count, 4, "big")
data = data + bytes.fromhex("00 11 22 33 44 55 66 77")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
print("data (len = %d) :" % (len(data)) )
print(data.hex(" ", 4))
c.update(data)
tag = c.finalize()
print("\ntag (len = %d) :" % (len(tag)))
print(tag.hex(" ", 4))
tagprime = tag[0:4]
print("\ntagprime (len = %d) : " % (len(tagprime)))
print(tagprime.hex(" ", 4))
print("\n\n")

count = count + 1
c  = cmac.CMAC(algorithms.AES(Sx))
data = int.to_bytes(count, 4, "big")
data = data + bytes.fromhex("00 11 22 33 44 55 66 77")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
data = data + bytes.fromhex("22 33 44 55 66 77 88 99")
data = data + bytes.fromhex("11 22 33 44 55 66 77 88")
print("data (len = %d) :" % (len(data)) )
print(data.hex(" ", 4))
c.update(data)
tag = c.finalize()
print("\ntag (len = %d) :" % (len(tag)))
print(tag.hex(" ", 4))
tagprime = tag[0:4]
print("\ntagprime (len = %d) : " % (len(tagprime)))
print(tagprime.hex(" ", 4))
print("\n\n")




