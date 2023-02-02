# adapter A
#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/

# msg = [ctr-mode encrypt | count]
#        --7 bytes------  | 1 byte

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

Sx =    bytes.fromhex("00000000 11111111 22222222 33333333")
nonce = bytes.fromhex("00000000 00000000 00000000 000000")

def adapter(msg):
   count = msg.data[7]

   cipher = Cipher(algorithms.AES(Sx), modes.ECB())
   encryptor = cipher.encryptor()
   iv =bytes(nonce) + count.to_bytes(1, "big")        # concatenate 
   ctiv = encryptor.update(iv) + encryptor.finalize()

   ct = msg.data[:7]
   pt = bytes([a ^ b for a, b in zip(ctiv, ct)])
   #print("adapterA -- pt : %s" %(pt.hex(" ",4)))
   data = pt + count.to_bytes(1, "big")
   msg.data = data 
   return msg

