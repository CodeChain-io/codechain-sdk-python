from jsondb.db import Database

from ..crypto import blake160
from ..crypto import generate_private_key
from ..crypto import get_account_id_from_public
from ..crypto import get_public_from_private
from ..crypto import sign_ecdsa
from .Errors import ErrorCode
from .Errors import KeystoreError
from .keys import key_from_public_key
from .KeyType import get_table_name
from .KeyType import KeyType
from .StorageJson import decode
from .StorageJson import encode


class keystoreManager:
    def __init__(self, key_type: KeyType, db):
        self.db = db
        self.key_type = key_type

    def get_keys(self) -> list:
        rows = self.db[self.key_type.value]
        return map(lambda storage: storage.address, rows)

    def import_raw(self, private_key: str, **kwargs):
        return self.__create_key_from_private_key(private_key, **kwargs)

    def export_key(self, key: str, passphrase: str):
        storage = self.get_storage(key)

        if storage is None:
            return None

        # Trows an error if the passphrase is incorrect
        decode(storage, passphrase)

        return storage

    def import_key(self, storage, passphrase: str):
        private_key = decode(storage, passphrase)
        return self.import_raw(private_key, passphrase=passphrase, meta=storage["meta"])

    def export_raw_key(self, key: str, passphrase: str):
        storage = self.get_storage(key)

        if storage is None:
            raise KeystoreError(ErrorCode.NOSUCHKEY)

        return decode(storage, passphrase)

    def get_public_key(self, key: str, passphrase: str):
        storage = self.get_storage(key)

        if storage is None:
            return None

        private_key = decode(storage, passphrase)
        return get_public_from_private(private_key)

    def create_key(self, **kwargs):
        private_key = generate_private_key()

        return self.__create_key_from_private_key(private_key, **kwargs)

    def delete_key(self, key: str):
        storage = self.get_storage(key)

        if storage is None:
            return None

        self.remove_key(key)

        return True

    def sign(self, key: str, message: str, passphrase: str):
        storage = self.get_storage(key)

        if storage is None:
            raise KeystoreError(ErrorCode.NOSUCHKEY)

        private_key = decode(storage, passphrase)

        return sign_ecdsa(message, private_key)

    def get_meta(self, key: str):
        storage = self.get_storage(key)

        if storage is None:
            raise KeystoreError(ErrorCode.NOSUCHKEY)

        return storage["meta"]

    def get_storage(self, key: str):
        rows = self.db[self.key_type.value]
        storage = list(filter(lambda storage: storage.address == key), rows)

        if len(storage) == 0:
            return None

        return storage

    def __create_key_from_private_key(self, private_key: str, **kwargs):
        passphrase = kwargs.get("passphrase", "")
        meta = kwargs.get("meta", "{}")

        public_key = get_public_from_private(private_key)
        storage = encode(private_key, self.key_type, passphrase, meta)

        self.db[self.key_type.value] = self.db[self.key_type.value] + [storage]
        return key_from_public_key(self.key_type, public_key)

    def remove_key(self, key: str):
        rows = self.db[self.key_type.value]
        filtered_rows = list(filter(lambda storage: storage.address != key), rows)
        self.db[self.key_type.value] = filtered_rows
