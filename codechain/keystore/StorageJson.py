import binascii
import os
import uuid

from Crypto.Cipher import AES
from Crypto.Util import Counter

from ..crypto import blake256
from ..crypto import get_public_from_private
from .keys import key_from_public_key
from .KeyType import KeyType
from .Pbkdf2 import pbkdf2


def encode(private_key: str, key_type: KeyType, passphrase: str, meta: str):
    public_key = get_public_from_private(private_key)
    address = key_from_public_key(key_type, public_key)
    salt = os.urandom(32)
    iv = os.urandom(16)

    kdf = "pbkdf2"
    kdf_params = {
        "dklen": 32,
        "salt": binascii.hexlify(salt).decode("ascii"),
        "c": 262144,
        "prf": "hmac-sha256",
    }
    derived_key = pbkdf2(
        passphrase.encode("utf-8"),
        salt,
        kdf_params.get("c"),
        kdf_params.get("dklen"),
        "sha256",
    )
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder="big"))
    cipher = AES.new(derived_key[:16], AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(private_key)
    mac = blake256(derived_key[16:32] + ciphertext)

    return {
        "crypto": {
            "ciphertext": binascii.hexlify(ciphertext).decode("ascii"),
            "cipherparams": {"iv": binascii.hexlify(iv).decode("ascii")},
            "cipher": "aes-128-ctr",
            "kdf": kdf,
            "kdfparams": kdf_params,
            "mac": mac,
        },
        "id": str(uuid.uuid4()),
        "version": 3,
        "address": address,
        "meta": meta,
    }
