from dataclasses import dataclass
from typing import List
from typing import Union

from rlp import encode

from .asset import Asset
from .assetmintoutput import AssetMintOutput
from .assetmintoutput import AssetMintOutputJSON
from .assetscheme import AssetScheme
from .transaction import AssetTransaction
from .transaction import Transaction
from codechain.crypto import blake160
from codechain.crypto import blake256
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import PlatformAddress


@dataclass
class AssetMintTransactionJSON:
    network_id: str
    shard_id: int
    metadata: str
    output: AssetMintOutputJSON
    approver: Union[str, None]
    registrar: Union[str, None]
    allowed_script_hashes: List[str]


@dataclass
class MintAssetActionJSON(AssetMintTransactionJSON):
    approvals: List[str]


class MintAsset(Transaction, AssetTransaction):
    def __init__(
        self,
        network_id: str,
        shard_id: int,
        metadata,
        output: AssetMintOutput,
        approver: Union[PlatformAddress, None],
        registrar: Union[PlatformAddress, None],
        allowed_script_hashes: Union[PlatformAddress, None],
        approvals: List[str],
    ):
        super().__init__(network_id)
        self._transaction = AssetMintTransaction(
            network_id,
            shard_id,
            metadata,
            output,
            approver,
            registrar,
            allowed_script_hashes,
        )
        self.approvals = approvals

    def tracker(self):
        return H256(blake256(self._transaction.rlp_bytes()))

    def add_approval(self, approval: str):
        self.approvals.append(approval)

    def output(self):
        return self._transaction.output

    def get_minted_asset(self):
        lock_script_hash = self._transaction.output.lock_script_hash
        parameters = self._transaction.output.parameters
        supply = self._transaction.output.supply

        if supply is None:
            raise ValueError("Not implemented")

        return Asset(
            self.tracker(),
            0,
            self.get_asset_type(),
            self._transaction.shard_id,
            supply,
            lock_script_hash,
            parameters,
        )

    def get_asset_scheme(self):
        if self._transaction.output.supply is None:
            raise ValueError("Not implemented")

        return AssetScheme(
            self._transaction.metadata,
            self._transaction.output.supply,
            self._transaction.approver,
            self._transaction.registrar,
            self._transaction.allowed_script_hashes,
            [],
            self._transaction.network_id,
            self._transaction.shard_id,
        )

    def get_asset_type(self):
        return H160(blake160(str(self.tracker())))

    def transaction_type(self):
        return "mintAsset"

    def action_to_encode_object(self):
        encoded = self._transaction.to_encode_object()
        encoded.append(self.approvals)
        return encoded

    def action_to_json(self):
        return self._transaction.to_json().update({"approvals": self.approvals})


class AssetMintTransaction:
    def __init__(
        self,
        network_id: str,
        shard_id: int,
        metadata,
        output: AssetMintOutput,
        approver: Union[PlatformAddress, None],
        registrar: Union[PlatformAddress, None],
        allowed_script_hashes: List[H160],
    ):
        self.network_id = network_id
        self.shard_id = shard_id
        self.metadata = metadata if isinstance(metadata, str) else str(metadata)
        self.output = output
        self.approver = approver
        self.registrar = registrar
        self.allowed_script_hashes = allowed_script_hashes

    def to_json(self):
        return {
            "networkId": self.network_id,
            "shardId": self.shard_id,
            "metadata": self.metadata,
            "output": self.output.to_json(),
            "approver": None if self.approver is None else str(self.approver),
            "registrar": None if self.registrar is None else str(self.registrar),
            "allowedScriptHash": map(lambda x: x.to_json(), self.allowed_script_hashes),
        }

    def to_encode_object(self):
        return [
            0x13,
            self.network_id,
            self.shard_id,
            self.metadata,
            self.output.lock_script_hash,
            map(lambda x: bytes(x), self.output.parameters),
            self.output.supply.to_encode_object(),
            []
            if self.approver is None
            else [self.approver.account_id.to_encoded_object()],
            []
            if self.registrar is None
            else [self.registrar.account_id.to_encoded_object()],
            map(lambda x: x.to_encode_object(), self.allowed_script_hashes),
        ]

    def rlp_bytes(self):
        return encode(self.to_encode_object())
