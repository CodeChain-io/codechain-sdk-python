from .assetmintoutput import AssetMintOutput
from .assettransferinput import AssetTransferInput
from .assettransferoutput import AssetTransferOutput
from .changeassetscheme import ChangeAssetScheme
from .createshard import CreateShard
from .custom import Custom
from .increaseassetsupply import IncreaseAssetSupply
from .mintasset import MintAsset
from .orderontransfer import OrderOnTranser
from .pay import Pay
from .remove import Remove
from .setregualrkey import SetRegularKey
from .setshardowners import SetShardOwners
from .setshardusers import SetShardUsers
from .signedtransaction import SignedTransaction
from .signedtransaction import SignedTransactionJSON
from .store import Store
from .transaction import Transaction
from .transferasset import TransferAsset
from .unwrapccc import UnwrapCCC
from .wrapccc import WrapCCC
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512
from codechain.primitives import PlatformAddress
from codechain.primitives import U64


def from_json_to_transaction(result: SignedTransactionJSON):
    seq = result.seq
    fee = result.fee
    network_id = result.network_id
    action = result.action
    action_type = result.action_type
    tx: Transaction

    if action_type == "mintAsset":
        raise ValueError("Not implemented")
    elif action_type == "changeAssetScheme":
        metadata = action.metadata
        approvals = action.approvals
        shard_id = action.shard_id

        asset_scheme_seq = action.seq
        asset_type = H160(action.asset_type)
        approver = (
            None if action.approver is None else PlatformAddress.ensure(action.approver)
        )
        registrar = (
            None
            if action.registrar is None
            else PlatformAddress.ensure(action.registrar)
        )
        allowed_script_hashes = list(
            map(lambda x: H160(x), action.allowed_script_hashes)
        )

        tx = ChangeAssetScheme(
            network_id,
            asset_type,
            shard_id,
            asset_scheme_seq,
            metadata,
            approver,
            registrar,
            allowed_script_hashes,
            approvals,
        )
    elif action_type == "increaseAssetSupply":
        raise ValueError("Not implemented")
    elif action_type == "transferAsset":
        raise ValueError("Not implemented")
    elif action_type == "unwrapCCC":
        raise ValueError("Not implemented")
    elif action_type == "pay":
        raise ValueError("Not implemented")
    elif action_type == "setRegularKey":
        raise ValueError("Not implemented")
    elif action_type == "createShard":
        raise ValueError("Not implemented")
    elif action_type == "setShardOwners":
        raise ValueError("Not implemented")
    elif action_type == "setShardUsers":
        raise ValueError("Not implemented")
    elif action_type == "wrapCCC":
        raise ValueError("Not implemented")
    elif action_type == "store":
        raise ValueError("Not implemented")
    elif action_type == "remove":
        raise ValueError("Not implemented")
    elif action_type == "custom":
        raise ValueError("Not implemented")
    else:
        raise ValueError(f"Unexpected action: {action}")

    if seq is not None:
        tx.seq = seq
    if fee is not None:
        tx.fee = fee

    return tx


def from_json_to_signed_transaction(data: SignedTransactionJSON):

    if not isinstance(data.sig, str):
        raise ValueError("Unexpected type of sig")

    if (
        data.block_number is not None
        and data.block_hash is not None
        and data.transaction_index is not None
    ):
        return SignedTransaction(
            from_json_to_transaction(data),
            data.sig,
            data.block_number,
            H256(data.block_hash),
            data.transaction_index,
        )
    else:
        return SignedTransaction(from_json_to_transaction(data), data.sig)
