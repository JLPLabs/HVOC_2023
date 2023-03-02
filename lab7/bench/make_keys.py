# create keys for adapter A and adapter B

import nacl.utils
from nacl.public import PrivateKey


# ----------------------------------------------------------

Ka = PrivateKey.generate()
Pa = Ka.public_key

print("\nCreating key pair files for adapter A")
ka_name = "Ka.key"
pa_name = "Pa.key"

# using 'with' construct will automatically close file
with open(ka_name, "wb") as key_file:
   
    # Write bytes to file
    key_file.write(bytes(Ka))
print("created: %s" % (ka_name))

with open(pa_name, "wb") as key_file:
   
    # Write bytes to file
    key_file.write(bytes(Pa))
print("created: %s" % (pa_name))


# ----------------------------------------------------------

Kb = PrivateKey.generate()
Pb = Kb.public_key

print("\nCreating key pair files for adapter B")
kb_name = "Kb.key"
pb_name = "Pb.key"

# using 'with' construct will automatically close file
with open(kb_name, "wb") as key_file:
   
    # Write bytes to file
    key_file.write(bytes(Kb))
print("created: %s" % (kb_name))

with open(pb_name, "wb") as key_file:
   
    # Write bytes to file
    key_file.write(bytes(Pb))
print("created: %s" % (pb_name))

