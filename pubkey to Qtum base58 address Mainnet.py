'''
pubkey to Qtum base58 address

References

https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses#How_to_create_Bitcoin_Address
https://stackoverflow.com/questions/59782364/sha256-giving-unexpected-result
https://docs.python.org/3/library/hashlib.html
'''

from binascii import unhexlify
import hashlib

# from functools import lru_cache
# from hashlib import sha256
# from typing import Mapping, Union

isMainnet = True    # flag for network prefix, set False for testnet & regtest
MAINNETPREFIX = "3a"            # hexadecimal
TESTNETREGTESTPREVIX = "78"     # hexadecimal

# from https://github.com/keis/base58/blob/master/base58/__init__.py

# 58 character alphabet used
BITCOIN_ALPHABET = \
    b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# Retro compatibility
alphabet = BITCOIN_ALPHABET

def b58encode_int(
    i: int, default_one: bool = True, alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    """
    Encode an integer using Base58
    """
    if not i and default_one:
        return alphabet[0:1]
    string = b""
    while i:
        i, idx = divmod(i, 58)
        string = alphabet[idx:idx+1] + string
    return string

# - - - - - - - - - - - - - - - - - - - - - - - - 

def main():

    # 1. Get the SHA256 hash of the bytestring pubkey

    pubkey = "03eb7062315dd132fb1c6cea6b629be85e6df23f40adc284b83db3a7fdc3d41d6d"
    bytestringPubkey = unhexlify(pubkey) # convert ASCII string to bytestring
    hashSHA256_step_1 = hashlib.sha256(bytestringPubkey).hexdigest() # get hexadecimal hash result
    print("1. hashSHA256_step_1 =", hashSHA256_step_1) # 1. hashSHA256_step_1 = 66c6f909582c167de94b74fae2da4f7ee3f57061aca72d24971399e5b25f29f4
    # 2. Get the RIPEMD-160 hash of #1

    bytestringhashRIPEMD160 = unhexlify(hashSHA256_step_1)
    hashRIPEMD160 = hashlib.new('ripemd160')
    hashRIPEMD160.update(bytestringhashRIPEMD160)
    hashRIPEMD160result = hashRIPEMD160.hexdigest()
    print("2. hashRIPEMD160 =", hashRIPEMD160result) # 2. hashRIPEMD160 = 81dc12de2866ea89a44b06ec58a01c604a3bae1b

    # 3. Add network version byte in front of RIPEMD-160 hash, 0x31 for Qtum mainnet and 0x78 for Qtum testnet and regtest

    if isMainnet == True:
        networkPrefix = MAINNETPREFIX           # mainnet
    else:
        networkPrefix = TESTNETREGTESTPREVIX    # testnet & regtest

    extendedRIPEMD160result = networkPrefix + hashRIPEMD160result

    print("3. extendedRIPEMD160result =", extendedRIPEMD160result) # 3. extendedRIPEMD160result = 3a81dc12de2866ea89a44b06ec58a01c604a3bae1b

    # 4. Get the SHA256 hash on the extended RIPEMD160 result

    bytestringExtendedRIPEMD160result = unhexlify(extendedRIPEMD160result)
    hashSHA256_step_4result = hashlib.sha256(bytestringExtendedRIPEMD160result).hexdigest()
    print("4. hashSHA256_step_4result =", hashSHA256_step_4result) # 4. hashSHA256_step_4result = b8d983392fa77dfeac21b9c89b9b0d5e4ce2a3b332b2ec885821b85f1053e791

    # 5. Get the SHA256 hash on the result step 4

    bytestringSHA256_step_4result = unhexlify(hashSHA256_step_4result)
    hashSHA256_step_5result = hashlib.sha256(bytestringSHA256_step_4result).hexdigest()
    print("5. hashSHA256_step_5result =", hashSHA256_step_5result) # 5. hashSHA256_step_5result = c0a05330558b8a9b2ffc7e56fb6b41107f4c774598f2e90ef342012596085387

    # 6. Take the first 4 bytes (8 characters) of step 4 as the checksum

    checksum = hashSHA256_step_5result[:8]  # get first 8 characters

    print("6. checksum =", checksum)           # 6. checksum = c0a05330

    # 7. Append the checksum to extendedRIPEMD160result from step 3. This is the 25-byte hex Qtum address.

    hexQtumAddress = "0" + extendedRIPEMD160result + checksum
    print("7. hexQtumAddress =", hexQtumAddress) # 7. hexQtumAddress = 03a81dc12de2866ea89a44b06ec58a01c604a3bae1bc0a05330

    # 8. Convert hexQtumAddress from step 7 to decimal and base58 encode

    decimalQtumAddress = int(hexQtumAddress, 16)

    byteQtumAddress = b58encode_int(decimalQtumAddress, BITCOIN_ALPHABET)

    print("8. byteQtumAddress =", byteQtumAddress)  # 8. byteQtumAddress = b'QYScv2vMxceXdTSqNtkahU92GJrEtafVMR'

    # 9. Convert byteQtumAddress to string QtumAddress

    QtumAddress = byteQtumAddress.decode("utf-8")

    print("9. QtumAddress =", QtumAddress)      # 9. QtumAddress = QYScv2vMxceXdTSqNtkahU92GJrEtafVMR


if __name__ == '__main__':
    main()




