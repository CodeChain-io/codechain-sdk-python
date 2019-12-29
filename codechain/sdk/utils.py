from dataclasses import dataclass
from typing import List
from typing import Union


@dataclass
class SignatureTag:
    inp: str
    outp: Union[str, List[int]]


def encode_signature_tag(tag: SignatureTag) -> bytes:
    tag_input = tag.inp
    tag_output = tag.outp

    if tag_input != "all" and tag_input != "single":
        raise ValueError(
            f"Expected the input of the tag to be either "
            "all"
            " or "
            "single"
            " but found {tag_input}"
        )

    input_mask = b"\x01" if tag_input == "all" else b"\x00"
    output_mask = b"\x01" if tag_output == "all" else b"\x00"

    if isinstance(tag_output, List):
        encoded = encode_signature_tag_output(tag_output.sort())

        if len(encoded) >= 64:
            raise ValueError("The output length is too big")

        return bytes([encoded] + [(len(encoded) << 2) | output_mask | input_mask])
    elif tag_output == "all":
        return bytes([output_mask | input_mask])
    else:
        raise ValueError(
            f"Expected the output of the tag to be either string "
            "all"
            " or an array of number but found {output}"
        )


def encode_signature_tag_output(output: List[int]):
    if output[0] < 0:
        raise ValueError(f"Invalid signature tag. Out of range: {output[0]}")
    elif output[len(output) - 1] > 503:
        raise ValueError(
            f"Invalid signature tag. Out of range: {output[output.length - 1]}"
        )

    offset = 0
    byte = 0
    sig_bytes = []

    for index in output:
        if not isinstance(index, int):
            raise ValueError(
                f"Expected an array of number but found {index} at {output[index]}"
            )

        if index < offset + 8:
            byte |= 1 << (index - offset)
        else:
            sig_bytes.append(byte)
            offset += 8
            while index >= offset + 8:
                sig_bytes.append(0)
                offset += 8
            byte = 1 << (index - offset)

    if byte != 0:
        sig_bytes.append(byte)

    return sig_bytes.reverse()
