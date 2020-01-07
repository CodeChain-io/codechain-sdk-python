from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Union

from rlp import encode

from ..utils import blake256
from ..utils import sign_ecdsa
from .changeassetscheme import ChangeAssetSchemeActionJSON
from .signedtransaction import SignedTransaction
from .transferasset import TransferAssetActionJSON
from codechain.primitives import H256
from codechain.primitives import U64


@dataclass
class TransactionJSON:
    action: Union[TransferAssetActionJSON, ChangeAssetSchemeActionJSON]
    action_type: str
    network_id: str
    seq: Union[int, None]
    fee: Union[str, None]


class AssetTransaction(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def tracker(self) -> H256:
        pass

    @abstractmethod
    def addApproval(self, approval: str):
        pass


class Transaction(ABC):
    def __init__(self, network_id: str):
        self.seq: int = None
        self.fee: U64 = None
        self.network_id = network_id
        super().__init__()

    def to_encode_object(self):
        if self.seq is None or self.fee is None:
            raise ValueError("Seq and fee in the tx must be present")
        return [
            self.seq,
            self.fee.to_encode_object(),
            self.network_id,
            self.action_to_encode_object(),
        ]

    def rlp_bytes(self):
        return encode(self.to_encode_object())

    def unsigned_hash(self):
        return H256(blake256(self.rlp_bytes()))

    def sign(self, secret: Union[H256, str], seq: int, fee: Union[U64, str]):
        if self.seq is not None:
            raise ValueError("The tx seq is already set")
        self.seq = seq

        if self.fee is not None:
            raise ValueError("The tx fee is already set")
        self.fee = U64(fee)

        return SignedTransaction(self, sign_ecdsa(self.unsigned_hash, H256(secret)))

    def to_json(self):
        action = self.action_to_json()
        result = {
            "networkId": self.network_id,
            "action": action.update({"type": self.transaction_type()}),
            "seq": self.seq,
            "fee": None if self.fee is None else self.fee.to_json(),
        }
        return result

    @abstractmethod
    def transaction_type(self):
        pass

    @abstractmethod
    def action_to_json(self):
        pass

    @abstractmethod
    def action_to_encode_object(self):
        pass
