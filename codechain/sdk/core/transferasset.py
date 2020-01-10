from dataclasses import dataclass
from typing import List
from typing import Union

from rlp import encode

from ..utils import blake128
from ..utils import blake256
from ..utils import blake256_with_key
from .asset import Asset
from .assettransferinput import AssetTransferInput
from .assettransferinput import AssetTransferInputJSON
from .assettransferoutput import AssetTransferOutput
from .assettransferoutput import AssetTransferOutputJSON
from .orderontransfer import OrderOnTranser
from .transaction import AssetTransaction
from .transaction import Transaction
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import U64


@dataclass
class AssetTransferTransactionJSON:
    pass


@dataclass
class TransferAssetActionJSON(AssetTransferTransactionJSON):
    metadata: str
    approvals: List[str]
    expiration: Union[int, None]


class TransferAsset:
    def __init__(
        self,
        burns: List[AssetTransferInput],
        inputs: List[AssetTransferInput],
        outputs: List[AssetTransferOutput],
        orders: List[OrderOnTranser],
        network_id: str,
        metadata,
        approvals: List[str],
        expiration: Union[int, None],
    ):
        pass
