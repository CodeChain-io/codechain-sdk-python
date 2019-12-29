from ..core.script import Script
from ..utils import encode_signature_tag
from ..utils import SignatureTag
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import H256


class P2PKH:
    def __init__(self, keystore, network_id: str):
        self.raw_keystore = keystore
        self.network_id = network_id

    @staticmethod
    def get_lock_script():
        return bytes(
            [
                Script.Opcode.get("COPY"),
                0x01,
                Script.Opcode.get("BLAKE160"),
                Script.Opcode.get("EQ"),
                Script.Opcode.get("JZ"),
                0xFF,
                Script.Opcode.get("CHKSIG"),
            ]
        )

    @staticmethod
    def get_lock_script_hash() -> H160:
        return H160("5f5960a7bca6ceeeb0c97bc717562914e7a1de04")

    def create_address(self, passphrase=None):
        key_hash = self.raw_keystore.asset.create_key(passphrase)
        return AssetAddress.from_type_and_payload(
            1, key_hash, network_id=self.network_id
        )

    def create_unlock_script(
        self,
        public_key_hash: str,
        signature_tag: SignatureTag,
        txhash: H256,
        passphrase=None,
    ):
        public_key = self.raw_keystore.get_public_key(passphrase, key=public_key_hash)
        if public_key is None:
            raise ValueError(
                f"Unable to get original key from the given public key hash: {public_key_hash}"
            )

        signature = self.raw_keystore.sign(
            passphrase, key=public_key_hash, message=txhash
        )
        encoded_tag = encode_signature_tag(signature_tag)
        PUSHB = Script.Opcode.get("PUSHB")

        return (
            bytes([PUSHB, 65])
            + bytes.fromhex(signature)
            + bytes([PUSHB, len(encoded_tag)])
            + encoded_tag
            + bytes([PUSHB, 64])
            + bytes.fromhex(public_key)
        )
