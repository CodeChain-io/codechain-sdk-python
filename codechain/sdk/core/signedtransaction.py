import binascii

from rlp import encode

from ..utils import recover_ecdsa
from .transaction import Transaction
from codechain.crypto import blake160
from codechain.crypto import blake256
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512
from codechain.primitives import PlatformAddress


class SignedTransaction:
    def __init__(
        self,
        unsigned: Transaction,
        signature: [bytes, bytearray],
        block_number: int = None,
        block_hash: H256 = None,
        transaction_index: int = None,
    ):
        self.unsigned = unsigned
        self.signature = signature
        self.block_number = block_number
        self.block_hash = block_hash
        self.transaction_index = transaction_index

    def to_encode_object(self):
        result = self.unsigned.to_encode_object()
        result.append("0x" + binascii.hexlify(self.signature).decode("ascii"))
        return result

    def rlp_bytes(self):
        encode(self.to_encode_object())

    def hash(self):
        return H256(blake256(self.rlp_bytes()))

    def get_asset(self):
        raise ValueError("Not implemented")

    def get_signer_account_id(self):
        public_key = recover_ecdsa(self.unsigned, self.signature)
        return H160(blake160(public_key))

    def get_signer_address(self, network_id: str):
        return PlatformAddress.from_account_id(
            self.get_signer_account_id(), network_id=network_id
        )

    def get_signer_public(self):
        return H512(recover_ecdsa(self.unsigned, self.signature))

    def to_json(self):
        json = self.unsigned.to_json().update(
            {
                "blockNumber": self.block_number,
                "blockHash": self.block_hash,
                "transactionIndex": self.transaction_index,
                "sig": "0x" + binascii.hexlify(self.signature).decode("ascii"),
                "hash": self.hash().to_json(),
            }
        )

        return json
