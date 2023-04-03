# source: https://github.com/dajiaji/python-cwt#cwt-with-pop-key
# docs:   https://python-cwt.readthedocs.io/en/stable/index.html


# ========================================================================
#      the OEM has a server ISSUING the CWT
# ========================================================================

import cwt
from cwt import COSEKey, Claims
import base64

# the public signing key here came from copy/paste of baler_ed25519-pub.txt
Pb_s_bytes = bytes.fromhex("a349a11d7f2b893c6eb636af6cf7e0a966d25cf3986020f77a0e9655459c5b74")
Pb_s_b64 = base64.b64encode(Pb_s_bytes)
Pb_s = str(Pb_s_b64, encoding="ascii")  # converts bytes to ascii expected in 'encode'
print(Pb_s)

# Read's the OEM's private signing key
with open("./oem_ed25519-priv.pem") as key_file:
    private_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    # Sets the PoP key to a CWT for the presenter.
    token = cwt.encode(
        {
            "iss": "oem.com",
            "sub": "baler1001",
            "aud": "tractor",
            "cnf": {
                "jwk": {  # Provided by the CWT presenter.
                    "kty": "OKP",
                    "use": "sig",
                    "crv": "Ed25519",
                    "kid": "presenter-01",
                    "x":   Pb_s,
                    "alg": "EdDSA",
                },
            },
        },
        private_key,
    )

f = open("pop.cwt", "wb")
f.write(token)
f.close()
# Issues the token to the presenter.



# ========================================================================
#      the baler uses the CWT to demonstrate "proof-of-possession" (PoP)
# ========================================================================

# Prepares a private PoP key in advance.
with open("./baler_ed25519-priv.pem") as key_file:
    pop_key_private = COSEKey.from_pem(key_file.read(), kid="presenter-01")

    # Receives a message (e.g., nonce)  from the recipient.
    msg = b"could-you-sign-this-message?"  # Provided by recipient.

    # Signs the message with the private PoP key.
    sig = pop_key_private.sign(msg)

# Sends the msg and the sig with the CWT to the recipient.

# create an invalid signature, in parallel; will 'verify' catch this? Yes!
invalidsig = bytes.fromhex("00") + sig[2:]

# ========================================================================
#      the tractor confirms the baler's "proof-of-possession" (PoP)
# ========================================================================

# Read the OEM's public key; so tractor can confirm CWT is valid
with open("./oem_ed25519-pub.pem") as key_file:
    public_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")

    # Validates and decodes the CWT received from the baler.
    raw = cwt.decode(token, public_key)
    decoded = Claims.new(raw)

    # Extracts the PoP key from the CWT.
    extracted_pop_key = COSEKey.new(decoded.cnf)  # = raw[8][1]

    # Then, verifies the message sent by the presenter
    # with the signature which is also sent by the presenter as follows:
    print(extracted_pop_key.verify(msg, sig))
    #print(extracted_pop_key.verify(msg, invalidsig))
