from .hash import blake160
from .key import get_public_from_private


def get_account_id_from_private(priv: bytes) -> str:
    public_key = get_public_from_private(priv)
    return get_account_id_from_public(public_key)


def get_account_id_from_public(public_key: bytes) -> str:
    return blake160(public_key)
