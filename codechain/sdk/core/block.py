import binascii
from dataclasses import dataclass
from typing import List

from rlp import encode

from .json import from_json_to_signed_transaction
from .signedtransaction import SignedTransaction
from .signedtransaction import SignedTransactionJSON
from codechain.primitives import H256
from codechain.primitives import PlatformAddress
from codechain.primitives import U256


@dataclass
class BlockJSON:
    parent_hash: str
    timestamp: int
    number: int
    author: str
    extra_data: List[int]
    transactions_root: str
    state_root: str
    score: str
    seal: List[List[int]]
    block_hash: str
    transactions: List[SignedTransactionJSON]


class Block:
    def __init__(
        self,
        parent_hash: H256,
        timestamp: int,
        number: int,
        author: PlatformAddress,
        extra_data: List[int],
        transactions_root: H256,
        state_root: H256,
        score: U256,
        seal: List[List[int]],
        block_hash: H256,
        transactions: List[SignedTransaction],
    ):
        self.parent_hash = parent_hash
        self.timestamp = timestamp
        self.number = number
        self.author = author
        self.extra_data = extra_data
        self.transactions_root = transactions_root
        self.state_root = state_root
        self.score = score
        self.seal = seal
        self.block_hash = block_hash
        self.transactions = transactions

    @staticmethod
    def from_json(data: BlockJSON):
        return Block(
            H256(data.parent_hash),
            data.timestamp,
            data.number,
            PlatformAddress.from_string(data.author),
            data.extra_data,
            H256(data.transactions_root),
            H256(data.state_root),
            U256(data.score),
            data.seal,
            H256(data.block_hash),
            list(map(from_json_to_signed_transaction, data.transactions)),
        )

    def to_json(self):
        return {
            "parentHash": self.parent_hash.to_json(),
            "timestamp": self.timestamp,
            "number": self.number,
            "author": str(self.author),
            "extraData": self.extra_data,
            "transactionsRoot": self.transactions_root.to_json(),
            "stateRoot": self.state_root.to_json(),
            "score": str(self.score),
            "seal": self.seal,
            "hash": self.block_hash.to_json(),
            "transactions": list(map(lambda x: x.to_json(), self.transactions)),
        }

    def get_size(self):
        block_header = []
        block_header.append(self.parent_hash.to_encode_object())
        block_header.append(self.author.account_id.to_encode_object())
        block_header.append(self.state_root.to_encode_object())
        block_header.append(self.transactions_root.to_encode_object())
        block_header.append(self.score.to_encode_object())
        block_header.append(self.number)
        block_header.append(self.timestamp)
        extra_data_to_str = binascii.hexlify(bytes(self.extra_data)).decode("ascii")
        block_header.append(f"0x{extra_data_to_str}")

        def seal_lambda(x):
            return "0x" + binascii.hexlify(bytes(x)).decode("ascii")

        block_header + list(map(seal_lambda, self.seal))

        encoded = encode(
            [block_header, list(map(lambda x: x.to_encode_object(), self.transactions))]
        )

        return len(encoded)
