# adapter B

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# For this lab adapterB "secures" an 8-byte Classic CAN J1939 message
# by encrypting the data bytes using AES-128 ECB and a given key Su.
# input: J1939 CAN msg structure
# output: encrypted J1939 CAN msg structure
def adapter(msg):
   Sx = bytes.fromhex("00000000 11111111 22222222 33333333")
   pad = bytes.fromhex("ffffffff ffffffff")
   cipher = Cipher(algorithms.AES(Sx), modes.ECB())
   encryptor = cipher.encryptor()
   pt = bytes(msg.data) + pad
   ct = encryptor.update(pt) + encryptor.finalize()
   msg.data = list(ct) 
   return msg
