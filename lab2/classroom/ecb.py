# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#interfaces

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = os.urandom(16)

# https://docs.python.org/3/library/stdtypes.html#bytes-objects

# https://docs.python.org/3/library/stdtypes.html#bytes.fromhex
# NOTE can use spaces and size the bytes as needed
key2 = bytes.fromhex("00000000 11111111 22222222 33333333")

# https://docs.python.org/3/library/stdtypes.html#bytes.hex
# NOTE can choose a seperator and number of bytes per seperator
print(key.hex(" ",4))
print(key2.hex(" ",4))

cipher = Cipher(algorithms.AES(key), modes.ECB())

encryptor = cipher.encryptor()
pt = b"0123456789abcdef"
ct = encryptor.update(pt) + encryptor.finalize()

decryptor = cipher.decryptor()
pt2 = decryptor.update(ct) + decryptor.finalize()

print(pt)
print(pt2)
