from ..crypto import blake160
from ..crypto import get_account_id_from_public
from .KeyType import KeyType


def key_from_public_key(key_type: KeyType, public_key: str) -> str:
    if key_type == KeyType.PLATFORM:
        return get_account_id_from_public(public_key)
    elif key_type == KeyType.ASSET:
        return blake160(public_key)
    else:
        raise ValueError("Invalid key type")
