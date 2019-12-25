import hashlib


def pbkdf2(passphrase: bytes, salt: bytes, iteration: int, keylen: int, digest: str):
    return hashlib.pbkdf2_hmac(digest, passphrase, salt, iteration, keylen)
