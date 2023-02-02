# adapter B
#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/

# msg = [ctr-mode encrypt | count]
#        --7 bytes------  | 1 byte

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

count = 0  # will range thru 0..255
Sx =    bytes.fromhex("00000000 11111111 22222222 33333333") # AES-128 key
nonce = bytes.fromhex("00000000 00000000 00000000 000000")   # nonce
# iv = nonce || count

def adapter(msg):
   global count
   count = count + 1

   cipher = Cipher(algorithms.AES(Sx), modes.ECB())
   encryptor = cipher.encryptor()
   iv =bytes(nonce) + count.to_bytes(1, "big")        # concatenate 
   ctiv = encryptor.update(iv) + encryptor.finalize()
   
   data = msg.data[:7]
   #print("adapterB -- data : %s" %(data.hex(" ",4)))
   ct = bytes([a ^ b for a, b in zip(ctiv, data)])
   data = ct + count.to_bytes(1, "big")
   msg.data = data
   return msg
