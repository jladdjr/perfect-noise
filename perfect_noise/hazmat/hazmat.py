############################################################
# hazmat.py                                                #
#                                                          #
# !!! WARNING !!!                                          #
# CONTAINS FUNCTIONS THAT ARE CRYPTOGRAPHICALLY SENSITIVE. #
############################################################

from operator import xor


def xor_encrypt(cleartext: bytes, key: bytes):
    assert len(cleartext) == len(key)
    return bytes(xor(i, j) for (i, j) in zip(cleartext, key))


xor_decrypt = xor_encrypt
