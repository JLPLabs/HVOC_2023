# adapter B
#
# reference:
# https://cryptography.io/en/latest/hazmat/primitives/mac/cmac/

# msg = [     data        | security overhead]
#        --7 bytes------  | ---  1 byte ----


def adapter(msg):
   return msg

