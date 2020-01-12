from dataclasses import dataclass
from typing import List
from typing import Union

from .assetmintoutput import AssetMintOutput
from .mintasset import MintAsset
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import PlatformAddress
from codechain.primitives import U64


@dataclass
class AssetSchemeJSON:
    metadata: str
    supply: str
    approver: str
    registrar: Union[str, None]
    allowed_script_hashes: Union[List[str], None]
    pool: List[dict]
    seq: int


class AssetScheme:
    def __init__(
        self,
        metadata,
        supply: U64,
        approver: Union[PlatformAddress, None],
        registrar: Union[PlatformAddress, None],
        allowed_script_hashes: List[H160],
        pool: List[dict],
        network_id: str = None,
        shard_id: int = None,
        seq: int = None,
    ):
        self.network_id = network_id
        self.shard_id = shard_id
        self.metadata = metadata if isinstance(metadata, str) else str(metadata)
        self.approver = approver
        self.registrar = registrar
        self.allowd_script_hashes = allowed_script_hashes
        self.supply = supply
        self.pool = pool
        self.seq = 0 if seq is None else seq

    @staticmethod
    def from_json(data: AssetSchemeJSON):
        return AssetScheme(
            data["metadata"],
            U64(data["supply"]),
            None
            if data["approver"] is None
            else PlatformAddress.ensure(data["approver"]),
            None
            if data["registrar"] is None
            else PlatformAddress.ensure(data["registrar"]),
            []
            if data["allowedScriptHashes"] is None
            else list(map(lambda x: H160(x), data["allowedScriptHashes"])),
            list(
                map(
                    lambda x: {
                        "assetType": H160(x["assetType"]),
                        "quantity": U64(x["quantity"]),
                    },
                    data["pool"],
                )
            ),
            None,
            None,
            data["seq"],
        )

    def to_json(self):
        return {
            "metadata": self.metadata,
            "supply": self.supply.to_json(),
            "approver": None if self.approver is None else str(self.approver),
            "registrar": None if self.registrar is None else str(self.registrar),
            "allowedScriptHashes": list(
                map(lambda x: x.to_json(), self.allowd_script_hashes)
            ),
            "pool": list(
                map(
                    lambda x: {
                        "assetType": x["assetType"].to_json(),
                        "quantity": x["quantity"].to_json(),
                    }
                )
            ),
            "seq": self.seq,
        }

    def create_mint_transaction(self, recipient: Union[AssetAddress, str]):
        if self.network_id is None:
            raise ValueError("networkId is undefined")
        if self.shard_id is None:
            raise ValueError("shardId is undefined")

        return MintAsset(
            self.network_id,
            self.shard_id,
            self.metadata,
            AssetMintOutput(self.supply, AssetAddress.ensure(recipient)),
            self.approver,
            self.registrar,
            self.allowd_script_hashes,
            [],
        )
