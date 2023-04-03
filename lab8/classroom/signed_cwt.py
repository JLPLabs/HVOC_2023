# source: https://github.com/dajiaji/python-cwt#signed-cwt 
#         https://github.com/dajiaji/python-cwt#cwt-with-user-defined-claims

from cwt import encode, decode, COSEKey, Claims, set_private_claim_names

# filename of OEM private and public signing keys
oem_k = "./oem_ed25519-priv.pem"
oem_p = "./oem_ed25519-pub.pem"

# TIM specific claims
tim_claim_names = {
    "func1": -70001,
    "func2": -70002,
    "func3": -70003,
    "func4": -70004,
    "func5": -70003,
    "func6": -70004,
}
set_private_claim_names(tim_claim_names)

# the sender side:
with open(oem_k) as key_file:
    private_key = COSEKey.from_pem(key_file.read(), kid="01")
    token = encode(
      {"iss": "oem.com", "sub": "baler1001", "aud": "TIMServer",
       "func5": True }, private_key
    )

# the recipient side:
with open(oem_p) as key_file:
    public_key = COSEKey.from_pem(key_file.read(), kid="01")
    decoded = decode(token, public_key)    # raw form
    readable = Claims.new(decoded, private_claim_names=tim_claim_names)
    print(decoded)
    print("iss: ", readable.get("iss"))
    print("sub: ", readable.get("sub"))
    print("aud: ", readable.get("aud"))
    print("exp: ", readable.get("exp"))
    print("func1: ", readable.get("func1"))
    print("func5: ", readable.get("func5"))


