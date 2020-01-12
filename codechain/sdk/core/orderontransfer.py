from dataclasses import dataclass
from typing import List

from rlp import encode

from .order import Order
from .order import OrderJSON
from codechain.primitives import U64


@dataclass
class OrderOnTransferJSON:
    order: OrderJSON
    spent_quantity: str
    input_from_indices: List[int]
    input_fee_indices: List[int]
    output_from_indices: List[int]
    output_to_indices: List[int]
    output_owned_fee_indices: List[int]
    output_transferred_fee_indices: List[int]


class OrderOnTranser:
    def __init__(
        self,
        order: Order,
        spent_quantity: U64,
        input_from_indices: List[int],
        input_fee_indices: List[int],
        output_from_indices: List[int],
        output_to_indices: List[int],
        output_owned_fee_indices: List[int],
        output_transferred_fee_indices: List[int],
    ):
        self.order = order
        self.spent_quantity = spent_quantity
        self.input_from_indices = input_from_indices
        self.input_fee_indices = input_fee_indices
        self.output_from_indices = output_from_indices
        self.output_to_indices = output_to_indices
        self.output_owned_fee_indices = output_owned_fee_indices
        self.output_transferred_fee_indices = output_transferred_fee_indices

    @staticmethod
    def from_json(data):
        return OrderOnTranser(
            Order.from_json(data["order"]),
            U64(data["spentQuantity"]),
            data["inputFromIndices"],
            data["inputFeeIndices"],
            data["outputFromIndices"],
            data["outputToIndices"],
            data["outputOwnedFeeIndices"],
            data["outputTransferredFeeIndices"],
        )

    def to_encode_object(self):
        return [
            self.order.to_encode_object(),
            self.spent_quantity.to_encode_object(),
            self.input_from_indices,
            self.input_fee_indices,
            self.output_from_indices,
            self.output_to_indices,
            self.output_owned_fee_indices,
            self.output_transferred_fee_indices,
        ]

    def rlp_bytes(self):
        return encode(self.to_encode_object())

    def to_json(self):
        return {
            "order": self.order.to_json(),
            "spentQuantioty": self.spent_quantity.to_json(),
            "inputFromIndices": self.input_from_indices,
            "inputFeeIndices": self.input_fee_indices,
            "outputFromIndices": self.output_from_indices,
            "outputToIndices": self.output_to_indices,
            "outputOwnedFeeIndices": self.output_owned_fee_indices,
            "outputTransferredFeeIndices": self.output_transferred_fee_indices,
        }

    def get_consumed_order(self):
        return self.order.consume(self.spent_quantity)
