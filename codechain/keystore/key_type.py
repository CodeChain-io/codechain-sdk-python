from enum import Enum


class KeyType(Enum):
    PLATFORM = "platform"
    ASSET = "asset"
    HDWSEED = "hdwseed"


def get_table_name(key_type: KeyType):
    return key_type.value
