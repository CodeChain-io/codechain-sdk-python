from typing import List
from typing import Union

from .assetmintoutput import AssetMintOutput
from codechain.primitives import PlatformAddress


class MintAsset:
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
        pass
