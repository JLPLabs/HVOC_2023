# adapter A

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# For this lab adapterA decrypts a "secure" J1939 message.
# where "secure" means it was encrypted using AES-128 ECB, using key Su.
# input: encrypted J1939 CAN msg structure
# output: J1939 CAN msg structure
def adapter(msg):
   Sx = bytes.fromhex("00000000 11111111 22222222 33333333")
   cipher = Cipher(algorithms.AES(Sx), modes.ECB())
   decryptor = cipher.decryptor()
   ct = bytes(msg.data)
   pt = decryptor.update(ct) + decryptor.finalize()
   msg.data = list(pt)[:8]    # strip off the padding
   return msg

