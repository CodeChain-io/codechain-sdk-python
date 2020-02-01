import binascii
from typing import List
from typing import Union

from ..core.asset import Asset
from ..core.assetscheme import AssetScheme
from ..core.block import Block
from ..core.json import from_json_to_signed_transaction
from ..core.signedtransaction import SignedTransaction
from ..core.text import Text
from ..core.transaction import Transaction
from .rpc import Rpc
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512
from codechain.primitives import PlatformAddress
from codechain.primitives import U64


class ChainRpc:
    def __init__(self, rpc: Rpc, transaction_signer: str = None):
        self.rpc = rpc
        self.transaction_signer = transaction_signer

    def send_transaction(
        self,
        tx: Transaction,
        account: PlatformAddress = None,
        passphrase: str = None,
        seq: Union[int, None] = None,
        fee: U64 = None,
        block_number: int = None,
    ):
        if not isinstance(tx, Transaction):
            raise ValueError(
                f"Expected the first argument of sendTransaction to be a Transaction but found {tx}"
            )

        account = self.transaction_signer if account is None else account
        fee = (
            self.get_mint_transaction_fee(tx.transaction_type(), block_number)
            if fee is None
            else fee
        )

        if account is None:
            raise ValueError("The account to sign the tx is not specified")
        elif not PlatformAddress.check(account):
            raise ValueError(
                f"Expected account param of sendTransaction to be a PlatformAddress value but found {account}"
            )

        seq = self.get_seq(account) if seq is None else seq

        tx.seq = seq

        if fee is None:
            raise ValueError("The fee of the tx is not specified")

        tx.fee = fee

        address = PlatformAddress.ensure(account)
        sig = self.rpc.account.sign(tx.unsigned_hash(), address, passphrase)

        return self.send_signed_transaction(SignedTransaction(tx, sig))

    def send_signed_transaction(self, tx: SignedTransaction):
        if not isinstance(tx, SignedTransaction):
            raise ValueError(
                f"Expected the first argument of sendSignedTransaction to be SignedTransaction but found {tx}"
            )

        return self.rpc.send_rpc_request(
            "mempool",
            "send_signed_transaction",
            "0x" + binascii.hexlify(tx.rlp_bytes()).decode("ascii"),
        )

    def get_mint_transaction_fee(
        self, transaction_type: str, block_number: Union[int, None] = None
    ):
        if block_number is not None and not block_number >= 0:
            raise ValueError(
                f"Expected the second argument of getMinTransactionFee to be non-negative integer but found {block_number}"
            )

        return self.rpc.send_rpc_request(
            "chain", "get_min_transaction_fee", transaction_type, block_number
        )

    def get_seq(self, address: PlatformAddress, block_number: int = None):
        if not PlatformAddress.check(address):
            raise ValueError(
                f"Expected the first argument of getSeq to be a PlatformAddress value but found {address}"
            )
        if block_number is not None and block_number >= 0:
            raise ValueError(
                f"Expected the second argument of getSeq to be a number but found ${block_number}"
            )

        return self.rpc.send_rpc_request(
            "chain", "get_seq", str(PlatformAddress.ensure(address)), block_number
        )

    def get_transaction_results_by_tracker(self, tracker: H256, timeout: int = None):
        if not H256.check(tracker):
            raise ValueError(
                f"Expected the first argument of getTransactionResultsByTracker to be an H256 value but found {tracker}"
            )

        if timeout is not None:
            raise ValueError("Not implemented")

        return self.rpc.send_rpc_request(
            "mempool", "get_transaction_results_by_tracker", "0x" + str(H256(tracker))
        )

    def contains_transaction(self, tx_hash: H256):
        if not H256.check(tx_hash):
            raise ValueError(
                f"Expected the first argument of containsTransaction to be an H256 value but found {tx_hash}"
            )

        result = self.rpc.send_rpc_request(
            "chain", "contains_transaction", "0x" + str(H256(tx_hash))
        )
        return result
