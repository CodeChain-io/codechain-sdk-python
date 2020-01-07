from dataclasses import dataclass
from typing import List
from typing import Union

from .asset import Asset
from .assetmintoutput import AssetMintOutput
from .assetoutpoint import AssetOutPoint
from .assetscheme import AssetScheme
from .assettransferinput import AssetTransferInput
from .assettransferinput import Timelock
from .assettransferoutput import AssetTransferOutput
from .block import Block
from .changeassetscheme import ChangeAssetScheme
from .createshard import CreateShard
from .custom import Custom
from .increaseassetsupply import IncreaseAssetSupply
from .mintasset import MintAsset
from .order import Order
from .orderontransfer import OrderOnTranser
from .pay import Pay
from .remove import Remove
from .script import Script
from .setregualrkey import SetRegularKey
from .setshardowners import SetShardOwners
from .setshardusers import SetShardUsers
from .signedtransaction import SignedTransaction
from .store import Store
from .transaction import Transaction
from .transferasset import TransferAsset
from .unwrapccc import UnwrapCCC
from .wrapccc import WrapCCC
from codechain.primitives import AssetAddress
from codechain.primitives import H128
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512
from codechain.primitives import PlatformAddress
from codechain.primitives import U256
from codechain.primitives import U64


@dataclass
class Classes:
    H128: type
    H160: type
    H256: type
    H512: type
    U256: type
    U64: type
    Block: type
    Transaction: type
    SignedTransaction: type
    Pay: type
    SetRegularKey: type
    CreateShard: type
    SetShardOwners: type
    SetShardUsers: type
    WrapCCC: type
    Store: type
    Remove: type
    Custom: type
    AssetTransferInput: type
    AssetTransferOutput: type
    AssetOutPoint: type
    Asset: type
    AssetScheme: type
    Script: type
    PlatformAddress: type
    AssetAddress: type


class Core:
    classes = Classes(
        H128,
        H160,
        H256,
        H512,
        U256,
        U64,
        Block,
        Transaction,
        SignedTransaction,
        Pay,
        SetRegularKey,
        CreateShard,
        SetShardOwners,
        SetShardUsers,
        WrapCCC,
        Store,
        Remove,
        Custom,
        AssetTransferInput,
        AssetTransferOutput,
        AssetOutPoint,
        Asset,
        AssetScheme,
        Script,
        PlatformAddress,
        AssetAddress,
    )

    def __init__(self, network_id: str):
        self.network_id = network_id

    def create_asset_scheme(
        self,
        shard_id: int,
        metadata,
        supply: U64,
        approver: PlatformAddress = None,
        registrar: PlatformAddress = None,
        allowed_script_hashes: List[H160] = None,
        pool: List[object] = None,
    ):
        if pool is None:
            pool = []

        check_metadata(metadata)
        metadata = metadata if isinstance(metadata, str) else str(metadata)
        check_shard_id(shard_id)
        check_amount(supply)
        check_approver(approver)
        check_registrar(registrar)

        return AssetScheme(
            metadata,
            U64(supply),
            None if approver is None else PlatformAddress.ensure(approver),
            None if registrar is None else PlatformAddress.ensure(registrar),
            [] if allowed_script_hashes is None else allowed_script_hashes,
            map(
                lambda x: {
                    "assetType": H160(x["assetType"]),
                    "quantity": U64(x["quantity"]),
                },
                pool,
            ),
            self.network_id,
            shard_id,
        )

    def create_mint_asset_transaction(
        self,
        scheme: AssetScheme,
        recipient: AssetAddress,
        approvals: List[str] = None,
        network_id: str = None,
        shard_id: int = None,
        metadata=None,
        approver: PlatformAddress = None,
        registrar: PlatformAddress = None,
        allowed_script_hashes: List[H160] = None,
        supply: U64 = None,
    ):
        if scheme is None and (shard_id is None or metadata is None):
            raise ValueError(
                f"Either scheme params or proper arguments should be provided {scheme}"
            )

        network_id = self.network_id if network_id is None else network_id
        shard_id = shard_id
        supply = U64(U64.MAX_VALUE) if supply is None else supply

        check_metadata(metadata)
        metadata = metadata if isinstance(metadata, str) else str(metadata)
        check_asset_address_recipient(recipient)
        check_network_id(network_id)
        if shard_id is None:
            raise ValueError("shard_id is None")
        check_shard_id(shard_id)
        check_approver(approver)
        check_registrar(registrar)
        check_amount(supply)

        return MintAsset(
            network_id,
            shard_id,
            metadata,
            AssetMintOutput(U64(supply), None, None, AssetAddress.ensure(recipient)),
            None if approver is None else PlatformAddress.ensure(approver),
            None if registrar is None else PlatformAddress.ensure(registrar),
            [] if allowed_script_hashes is None else allowed_script_hashes,
            approvals,
        )


def check_metadata(metadata):
    if not isinstance(metadata, (str, dict)) and metadata is not None:
        raise ValueError(
            f"Expected metadata param to be either a string or an object but found {metadata}"
        )


def check_shard_id(shard_id: int):
    if not isinstance(shard_id, int) or shard_id < 0 or shard_id > 0xFFFF:
        raise ValueError(f"Expected shardId param to be a number but found {shard_id}")


def check_amount(amount: U64):
    if not U64.check(amount):
        raise ValueError(f"Expected amount param to be a U64 value but found ${amount}")


def check_approver(approver: Union[None, PlatformAddress]):
    if approver is not None and not PlatformAddress.check(approver):
        raise ValueError(
            f"Expected approver param to be either null or a PlatformAddress value but found ${approver}"
        )


def check_registrar(registrar: Union[None, PlatformAddress]):
    if registrar is not None and not PlatformAddress.check(registrar):
        raise ValueError(
            f"Expected registrar param to be either null or a PlatformAddress value but found ${registrar}"
        )


def check_asset_address_recipient(recipient: AssetAddress):
    if not AssetAddress.check(recipient):
        raise ValueError(
            f"Expected recipient param to be a AssetAddress but found {recipient}"
        )


def check_network_id(network_id: str):
    if not isinstance(network_id, str) or len(network_id) != 2:
        raise ValueError(
            f"Expected networkId param to be a string of length 2 but found {network_id}"
        )
