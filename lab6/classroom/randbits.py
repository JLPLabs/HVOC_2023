import secrets

x = secrets.randbits(8)
print(x)

x = secrets.randbits(64)
xb = x.to_bytes(8, "big")        # converts 64 bits into 8 bytes
print(xb.hex(" ", 4))            # example: 61e015f7 920a8f0a
