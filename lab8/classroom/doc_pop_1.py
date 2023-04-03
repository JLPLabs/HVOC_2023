# debugging purposes
# copy directly from github PoP example
# https://github.com/dajiaji/python-cwt#cwt-with-pop-key

import cwt
from cwt import COSEKey
import base64


# Prepares a signing key for CWT in advance.
#with open("./private_key_of_issuer.pem") as key_file:
with open("./oem_ed25519-priv.pem") as key_file:
    private_key = COSEKey.from_pem(key_file.read(), kid="issuer-01")
    # the public signing key here came from copy/paste of baler_ed25519-pub.txt
    x1 = base64.b64encode(bytes.fromhex("a349a11d7f2b893c6eb636af6cf7e0a966d25cf3986020f77a0e9655459c5b74"))
    print(x1)
    print(type(x1))
    x2 = str(x1, encoding="ascii")
    print(x2)
    print(type(x2))

    x = "2E6dX83gqD_D0eAmqnaHe1TC1xuld6iAKXfw2OVATr0"
    print(x)
    print(type(x))

# Sets the PoP key to a CWT for the presenter.
token = cwt.encode(
    {
        "iss": "coaps://as.example",
        "sub": "dajiaji",
        "cti": "123",
        "cnf": {
            "jwk": {  # Provided by the CWT presenter.
                "kty": "OKP",
                "use": "sig",
                "crv": "Ed25519",
                "kid": "presenter-01",
#                "x": "2E6dX83gqD_D0eAmqnaHe1TC1xuld6iAKXfw2OVATr0",
                "x": x2,
                "alg": "EdDSA",
            },
        },
    },
    private_key,
)
