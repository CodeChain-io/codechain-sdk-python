from dataclasses import dataclass
from typing import Union

from ..core.signedtransaction import SignedTransaction
from ..core.transaction import AssetTransaction
from ..core.transaction import Transaction
from .localkeystore import LocalKeyStore
from .memorykeystore import MemoryKeyStore
from .p2pkh import P2PKH
from .p2pkhburn import P2PKHBurn
from .remotekeystore import RemoteKeyStore
from codechain.primitives import PlatformAddress
from codechain.primitives import U64


@dataclass
class KeyStoreType:
    keystore_type: str
    url_or_path: Union[str, None]


class Key:
    def __init__(self, network_id: str, key_store_type: KeyStoreType):
        if not is_keystore_type(key_store_type):
            raise ValueError(f"Unexpected keyStoreType param: {key_store_type}")
        self.network_id = network_id
        self.keystore = None
        self.keystore_type = key_store_type

    def create_remote_keystore(self, keystore_url: str):
        raise ValueError("Not implemented")

    def create_local_keystore(self, db_path: str = None):
        return LocalKeyStore.create(db_path)

    def create_platform_address(self, keystore=None, passphrase=""):
        keystore = self.ensure_keystore()
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )

        account_id = keystore.platform.create_key(passphrase=passphrase)
        network_id = self.network_id

        return PlatformAddress.from_account_id(account_id, network_id=network_id)

    def create_asset_address(self, addr_type="P2PKH", keystore=None, passphrase=""):
        keystore = self.ensure_keystore()
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )
        network_id = self.network_id

        if addr_type == "P2PKH":
            p2pkh = P2PKH(keystore, network_id)
            return p2pkh.create_address(passphrase)
        elif addr_type == "P2PKHBurn":
            p2pkhburn = P2PKHBurn(keystore, network_id)
            return p2pkhburn.create_address(passphrase)
        else:
            raise ValueError(
                f"Expected the type param of createAssetAddress to be either P2PKH or P2PKHBurn but found {addr_type}"
            )

    def create_p2pkh(self, keystore):
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )

        return P2PKH(keystore, self.network_id)

    def create_p2pkhburn(self, keystore):
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )

        return P2PKHBurn(keystore, self.network_id)

    def approve_transaction(
        self,
        account: Union[str, PlatformAddress],
        transaction: AssetTransaction,
        keystore=None,
        passphrase="",
    ):
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )

        if not PlatformAddress.check(account):
            raise ValueError(
                f"Expected account param to be a PlatformAddress value but found {account}"
            )

        account_id = PlatformAddress.ensure(account).account_id

        return keystore.platform.sign(
            account_id.to_string(), transaction.tracker(), passphrase
        )

    def sign_transaction(
        self,
        tx: Transaction,
        account: Union[PlatformAddress, str],
        fee: Union[U64, str, int],
        seq: int,
        keystore=None,
        passphrase="",
    ):
        if not isinstance(tx, Transaction):
            raise ValueError(
                f"Expected the first argument of signTransaction to be a Transaction instance but found {tx}"
            )

        keystore = self.ensure_keystore()
        if not is_keystore(keystore):
            raise ValueError(
                f"Expected keyStore param to be a KeyStore instance but found {keystore}"
            )
        if not PlatformAddress.check(account):
            raise ValueError(
                f"Expected account param to be a PlatformAddress value but found {account}"
            )
        if not U64.check(fee):
            raise ValueError(f"Expected fee param to be a U64 value but found {fee}")
        if not isinstance(seq, int):
            raise ValueError(f"Expected seq param to be a number value but found {seq}")
        tx.fee = fee
        tx.seq = seq
        account_id = PlatformAddress.ensure(account).account_id
        sig = keystore.platform.sign(
            account_id.to_string(), tx.unsigned_hash(), passphrase
        )

        return SignedTransaction(tx, sig)

    def sign_transaction_input(self):
        raise ValueError("Not implemented")

    def sign_transaction_input_with_order(self):
        raise ValueError("Not implemented")

    def sign_transaction_burn(self):
        raise ValueError("Not implemented")

    def ensure_keystore(self):
        if self.keystore is None:
            if self.keystore_type == "local":
                self.keystore = LocalKeyStore.create()
            elif self.keystore_type.type == "local":
                self.keystore = LocalKeyStore.create(self.keystore_type.url_or_path)
            else:
                raise ValueError("Not implemented")
        return self.keystore


def is_keystore(value):
    if isinstance(value, RemoteKeyStore):
        raise ValueError("Not implemented")
    if isinstance(value, MemoryKeyStore):
        raise ValueError("Not implemented")
    return isinstance(value, LocalKeyStore)


def is_keystore_type(value: KeyStoreType):
    if not isinstance(value, KeyStoreType):
        return False

    if value.url_or_path is None:
        if value == "local":
            return True
        elif value == "memory":
            raise ValueError("Not implemented")
        else:
            return False
    else:
        if value.type == "local" and isinstance(value.url_or_path, str):
            return True
        elif value.type == "remote":
            raise ValueError("Not implemented")
        else:
            return False
