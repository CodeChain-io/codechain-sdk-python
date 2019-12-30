from .transaction import Transaction
from codechain.primitives import H256


class SignedTransaction:
    def __init__(
        self,
        unsigned: Transaction,
        signature: str,
        block_number: int = None,
        block_hash: H256 = None,
        transaction_index: int = None,
    ):
        self.unsigned = unsigned
        self.signature = signature[2:] if signature.startswith("0x") else signature
        self.block_number = block_number
        self.block_hash = block_hash
        self.transaction_index = transaction_index
