# generate Ed25519 signing keys
#  -- private keys --
openssl genpkey -algorithm ed25519 -out oem_ed25519-priv.pem 
openssl genpkey -algorithm ed25519 -out hack_ed25519-priv.pem 
openssl genpkey -algorithm ed25519 -out baler_ed25519-priv.pem 
openssl genpkey -algorithm ed25519 -out tract_ed25519-priv.pem 
#  -- public keys --
openssl pkey -in oem_ed25519-priv.pem   -pubout -out oem_ed25519-pub.pem
openssl pkey -in hack_ed25519-priv.pem  -pubout -out hack_ed25519-pub.pem
openssl pkey -in baler_ed25519-priv.pem -pubout -out baler_ed25519-pub.pem
openssl pkey -in tract_ed25519-priv.pem -pubout -out tract_ed25519-pub.pem
#  -- text version of baler public key --
openssl pkey -in baler_ed25519-priv.pem -pubout -text -out baler_ed25519-pub.txt


# generate X25519 key agreement keys
#  -- private keys --
openssl genpkey -algorithm x25519 -out baler_x25519-priv.pem
openssl genpkey -algorithm x25519 -out tract_x25519-priv.pem
#  -- public keys --
openssl pkey -in baler_x25519-priv.pem -pubout -out baler_x25519-pub.pem
openssl pkey -in tract_x25519-priv.pem -pubout -out tract_x25519-pub.pem


# output in a non-encoded form of signing keys
openssl pkey -in oem_ed25519-priv.pem   -text -noout > oem_ed25519.keys 
openssl pkey -in hack_ed25519-priv.pem  -text -noout > hack_ed25519.keys 
openssl pkey -in baler_ed25519-priv.pem -text -noout > baler_ed25519.keys 
openssl pkey -in tract_ed25519-priv.pem -text -noout > tract_ed25519.keys 


ls -alrt

