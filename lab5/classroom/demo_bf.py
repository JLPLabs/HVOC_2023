import blowfish

cipher = blowfish.Cipher(b"Key must be between 4 and 56 bytes long.")


from os import urandom

block = urandom(8)

ciphertext = cipher.encrypt_block(block)
plaintext = cipher.decrypt_block(ciphertext)

assert block == plaintext
