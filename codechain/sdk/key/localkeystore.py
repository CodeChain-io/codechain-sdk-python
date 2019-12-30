from typing import Union

from codechain.keystore import CCkey


class LocalKeyStore:
    def __init__(self, cckey: CCkey):
        self.cckey = cckey
        self.platform = Platform(cckey)
        self.asset = Asset(cckey)

    @staticmethod
    def create(db_path=None):
        if db_path is not None:
            cckey = CCkey.create(db_path=db_path)
        else:
            cckey = CCkey.create()

        return LocalKeyStore(cckey)

    def close(self):
        return self.cckey.close()


class Platform:
    def __init__(self, cckey: CCkey):
        self.cckey = cckey

    def get_key_list(self):
        return self.cckey.platform.get_keys()

    def create_key(self, passphrase=""):
        return self.cckey.platform.create_key(passphrase=passphrase)

    def remove_key(self, key: str):
        return self.cckey.platform.delete_key(key)

    def export_raw_key(self, key: str, passphrase=""):
        return self.cckey.platform.export_raw_key(key, passphrase)

    def get_public_key(self, key: str, passphrase=""):
        return self.cckey.platform.get_public_key(key, passphrase)

    def sign(self, key: str, message: Union[bytearray, bytes], passphrase=""):
        return self.cckey.platform.sign(key, message, passphrase)


class Asset:
    def __init__(self, cckey: CCkey):
        self.cckey = cckey

    def get_key_list(self):
        return self.cckey.asset.get_keys()

    def create_key(self, passphrase=""):
        return self.cckey.asset.create_key(passphrase=passphrase)

    def remove_key(self, key: str):
        return self.cckey.asset.delete_key(key)

    def export_raw_key(self, key: str, passphrase=""):
        return self.cckey.asset.export_raw_key(key, passphrase)

    def get_public_key(self, key: str, passphrase=""):
        return self.cckey.asset.get_public_key(key, passphrase)

    def sign(self, key: str, message: Union[bytearray, bytes], passphrase=""):
        return self.cckey.asset.sign(key, message, passphrase)
