# source:
# https://pyjwt.readthedocs.io/en/stable/
# https://auth0.com/blog/how-to-handle-jwt-in-python/

import jwt
from cryptography.hazmat.primitives import serialization

# JWT has 3 components
#  * header     (contains claims)
#  * payload    (contains claims re: the roles that have been authorized)
#  * signature  (used by resource to validate the JWT)

# JSON format
payload_data  = {

	"sub": "baler-model1-pin1042",

	"name": "Baler Model1 Pin1042",

	"roles": ["func4", "func6"],
}


# to sign the JWT with our Ed25519 we need to read key
private_key = open('oem_ed25519', 'r').read()
Koem = serialization.load_ssh_private_key(private_key.encode(), 
	password=b'')


# create the function token
func_token = jwt.encode(

	payload=payload_data,

	key=Koem,

	algorithm='EdDSA'
)

print(func_token)
print()
print("now to verify the token, using the OEM public key")
public_key = open('oem_ed25519.pub', 'r').read()
hacker_key = open('hack_ed25519.pub', 'r').read()
Poem = serialization.load_ssh_public_key(public_key.encode())
Phak = serialization.load_ssh_public_key(hacker_key.encode())
# IMPORTANT... tell the library that you want the token validated before
#              using the token!
options = {"verify_signature":True}
result = jwt.decode(jwt=func_token, key=Poem, algorithms=["EdDSA"],
         options=options)

print(result)
print("\n\n")
print("note: can demonstrate failed validation of JWT by using Phak")
print("      in the call to jwt.decode()")

