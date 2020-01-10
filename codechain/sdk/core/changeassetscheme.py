from dataclasses import dataclass
from typing import List
from typing import Union

from rlp import encode

from ..utils import blake256
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import PlatformAddress


@dataclass
class AssetSchemeChangeTransactionJSON:
    network_id: str
    shard_id: int
    asset_type: str
    seq: int
    metadata: str
    approver: Union[str, None]
    registrar: Union[str, None]
    allowed_script_hashes: List[str]


@dataclass
class ChangeAssetSchemeActionJSON(AssetSchemeChangeTransactionJSON):
    approvals: List[str]

from .transaction import Transaction
class ChangeAssetScheme(Transaction):
    def __init__(
        self,
        network_id: str,
        asset_type: H160,
        shard_id: int,
        seq: int,
        metadata,
        approver: Union[PlatformAddress, None],
        registrar: Union[PlatformAddress, None],
        allowed_script_hashes: List[H160],
        approvals: List[str],
    ):
        super().__init__(network_id)
        self._transaction = AssetSchemeChangeTransaction(
            network_id,
            shard_id,
            asset_type,
            seq,
            metadata,
            approver,
            registrar,
            allowed_script_hashes,
        )
        self.approvals = approvals

    def tracker(self) -> H256:
        return H256(blake256(self._transaction.rlp_bytes()))

    def add_approval(self, approval: str):
        self.approvals.append(approval)

    def transaction_type(self):
        return "changeAssetScheme"

    def action_to_encode_object(self):
        encoded = self._transaction.to_encode_object()
        encoded.append(self.approvals)
        return encode

    def action_to_json(self):
        json = self._transaction.to_json()
        return json.update({"approvals": self.approvals})


class AssetSchemeChangeTransaction:
    def __init__(
        self,
        network_id: str,
        shard_id: int,
        asset_type: H160,
        seq: int,
        metadata,
        approver: Union[PlatformAddress, None],
        registrar: Union[PlatformAddress, None],
        allowed_script_hashes: List[H160],
    ):
        self.network_id = network_id
        self.shard_id = shard_id
        self.asset_type = asset_type
        self.seq = seq
        self.metatdata = metadata if isinstance(metadata, str) else str(metadata)
        self.approver = None if approver is None else PlatformAddress.ensure(approver)
        self.registrar = (
            None if registrar is None else PlatformAddress.ensure(registrar)
        )
        self.allowed_script_hashes = allowed_script_hashes

    def to_json(self):
        return {
            "networkId": self.network_id,
            "shardId": self.shard_id,
            "assetType": self.asset_type.to_encode_object(),
            "seq": self.seq,
            "metadata": self.metatdata,
            "approver": None if self.approver is None else str(self.approver),
            "registrar": None if self.registrar is None else str(self.registrar),
            "allowedScriptHashes": map(
                lambda x: x.to_json(), self.allowed_script_hashes
            ),
        }

    def to_encode_object(self):
        return [
            0x15,
            self.network_id,
            self.shard_id,
            self.asset_type.to_encode_object(),
            self.seq,
            self.metatdata,
            None
            if self.approver is None
            else [self.approver.account_id.to_encode_object()],
            None
            if self.registrar is None
            else [self.registrar.account_id.to_encode_object()],
            map(lambda x: x.to_encode_object(), self.allowed_script_hashes),
        ]

    def rlp_bytes(self):
        return encode(self.to_encode_object())
