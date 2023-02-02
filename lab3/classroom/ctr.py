#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

count = 0  # will range thru 0..255

Sx =    bytes.fromhex("00000000 11111111 22222222 33333333")
nonce = bytes.fromhex("00000000 00000000 00000000 000000")
count = count + 1  
iv = bytes(nonce) + count.to_bytes(1, "big")
print("iv")
print(iv.hex(" ", 4))

cipher = Cipher(algorithms.AES(Sx), modes.ECB())
encryptor = cipher.encryptor()
ctiv = encryptor.update(iv) + encryptor.finalize()
print("ctiv")
print(ctiv.hex(" ", 4))

data = bytes.fromhex("dead cafe beef 0102")
ct = bytes([a ^ b for a, b in zip(ctiv, data)])
print("ct")
print(ct.hex(" ", 4))

print("now, to decrypt...")
pt = bytes([a ^ b for a, b in zip(ctiv, ct)])
print("pt")
print(pt.hex(" ", 4))

