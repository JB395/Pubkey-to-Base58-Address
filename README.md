# Pubkey-to-Base58-Address
Public key to base58 address

Convert a Qtum public key, for example, a block reward payment, to a Qtum base58 address in 9 steps:

1. Get the SHA256 hash of the bytestring pubkey
2. Get the RIPEMD-160 hash of #1
3. Add network version byte in front of RIPEMD-160 hash, 0x31 for Qtum mainnet and 0x78 for Qtum testnet and regtest
4. Get the SHA256 hash on the extended RIPEMD160 result
5. Get the SHA256 hash on the result step 4
6. Take the first 4 bytes (8 characters) of step 4 as the checksum
7. Append the checksum to extendedRIPEMD160result from step 3. This is the 25-byte hex Qtum address.
8. Convert hexQtumAddress from step 7 to decimal and base58 encode
9. Convert byteQtumAddress to string QtumAddress
