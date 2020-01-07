from typing import Union

from .hash import blake160
from .key import get_public_from_private


def get_account_id_from_private(priv: Union[bytes, bytearray, str]) -> bytes:
    public_key = get_public_from_private(priv)
    return get_account_id_from_public(public_key)


def get_account_id_from_public(public_key: Union[bytearray, bytes, str]) -> bytes:
    return blake160(public_key)
