"""
Recursive Length Prefix (RLP) Encoding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. contents:: Table of Contents
    :backlinks: none
    :local:

Introduction
------------

Defines the serialization and deserialization format used throughout Ethereum.
"""

from __future__ import annotations

from typing import List, Sequence, Union, cast

from .base_types import U256, Uint
from .eth_types import Bytes

RLP = Union[Bytes, Uint, U256, Sequence["RLP"]]  # type: ignore


#
# RLP Encode
#


def encode(raw_data: RLP) -> Bytes:
    """
    Encodes `raw_data` into a sequence of bytes using RLP.

    Parameters
    ----------
    raw_data : `RLP`
        A `Bytes`, `Uint`, `Uint256` or sequence of `RLP` encodable
        objects.

    Returns
    -------
    encoded : `eth1spec.eth_types.Bytes`
        The RLP encoded bytes representing `raw_data`.
    """
    if isinstance(raw_data, (bytearray, bytes)):
        return encode_bytes(raw_data)
    elif isinstance(raw_data, (Uint, U256)):
        return encode(raw_data.to_be_bytes())
    elif isinstance(raw_data, str):
        return encode_bytes(raw_data.encode())
    elif isinstance(raw_data, Sequence):
        return encode_sequence(cast(Sequence[RLP], raw_data))
    else:
        raise TypeError(
            "RLP Encoding of type {} is not supported".format(type(raw_data))
        )


def encode_bytes(raw_bytes: Bytes) -> Bytes:
    """
    Encodes `raw_bytes`, a sequence of bytes, using RLP.

    Parameters
    ----------
    raw_bytes : `eth1spec.eth_types.Bytes`
        Bytes to encode with RLP.

    Returns
    -------
    encoded : `eth1spec.eth_types.Bytes`
        The RLP encoded bytes representing `raw_bytes`.
    """
    len_raw_data = Uint(len(raw_bytes))

    if len_raw_data == 1 and raw_bytes[0] < 0x80:
        return raw_bytes
    elif len_raw_data < 0x38:
        return bytearray([128 + len_raw_data]) + raw_bytes
    else:
        # length of raw data represented as big endian bytes
        len_raw_data_as_be = len_raw_data.to_be_bytes()
        return (
            bytearray([183 + len(len_raw_data_as_be)])
            + len_raw_data_as_be
            + raw_bytes
        )


def encode_sequence(raw_sequence: Sequence[RLP]) -> Bytes:
    """
    Encodes a list of RLP encodable objects (`raw_sequence`) using RLP.

    Parameters
    ----------
    raw_sequence : `Sequence[RLP]`
            Sequence of RLP encodable objects.

    Returns
    -------
    encoded : `eth1spec.eth_types.Bytes`
        The RLP encoded bytes representing `raw_sequence`.
    """
    joined_encodings = get_joined_encodings(raw_sequence)
    len_joined_encodings = Uint(len(joined_encodings))

    if len_joined_encodings < 0x38:
        return bytearray([192 + len_joined_encodings]) + joined_encodings
    else:
        len_joined_encodings_as_be = len_joined_encodings.to_be_bytes()
        return (
            bytearray([247 + len(len_joined_encodings_as_be)])
            + len_joined_encodings_as_be
            + joined_encodings
        )


def get_joined_encodings(raw_sequence: Sequence[RLP]) -> Bytes:
    """
    Obtain concatenation of rlp encoding for each item in the sequence
    raw_sequence.

    Parameters
    ----------
    raw_sequence : `Sequence[RLP]`
        Sequence to encode with RLP.

    Returns
    -------
    joined_encodings : `eth1spec.eth_types.Bytes`
        The concatenated RLP encoded bytes for each item in sequence
        raw_sequence.
    """
    joined_encodings = bytearray()
    for item in raw_sequence:
        joined_encodings += encode(item)

    return joined_encodings


#
# RLP Decode
#


def decode(encoded_data: Bytes) -> RLP:
    """
    Decodes an integer, byte sequence, or list of RLP encodable objects
    from the byte sequence `encoded_data`, using RLP.

    Parameters
    ----------
    encoded_data : `eth1spec.eth_types.Bytes`
        A sequence of bytes, in RLP form.

    Returns
    -------
    decoded_data : `RLP`
        Object decoded from `encoded_data`.
    """
    # Raising error as there can never be empty encoded data for any
    # given raw data (including empty raw data)
    # RLP Encoding(b'') -> [128]
    # RLP Encoding([]) -> [192]
    assert len(encoded_data) > 0

    if encoded_data[0] <= 0xBF:
        # This means that the raw data is of type bytes
        return decode_to_bytes(encoded_data)
    else:
        # This means that the raw data is of type sequence
        return decode_to_sequence(encoded_data)


def decode_to_bytes(encoded_bytes: Bytes) -> Bytes:
    """
    Decodes a rlp encoded byte stream assuming that the decoded data
    should be of type `bytes`.

    Parameters
    ----------
    encoded_bytes : `eth1spec.eth_types.Bytes`
        RLP encoded byte stream.

    Returns
    -------
    decoded : `eth1spec.eth_types.Bytes`
        RLP decoded Bytes data
    """
    if len(encoded_bytes) == 1 and encoded_bytes[0] < 0x80:
        return encoded_bytes
    elif encoded_bytes[0] <= 0xB7:
        len_raw_data = encoded_bytes[0] - 128
        assert len_raw_data < len(encoded_bytes)
        raw_data = encoded_bytes[1 : 1 + len_raw_data]
        assert not (len_raw_data == 1 and raw_data[0] < 0x80)
        return raw_data
    else:
        # This is the index in the encoded data at which decoded data
        # starts from.
        decoded_data_start_idx = 1 + encoded_bytes[0] - 183
        assert decoded_data_start_idx - 1 < len(encoded_bytes)
        # Expectation is that the big endian bytes shouldn't start with 0
        # while trying to decode using RLP, in which case is an error.
        assert encoded_bytes[1] != 0
        len_decoded_data = Uint.from_be_bytes(
            encoded_bytes[1:decoded_data_start_idx]
        )
        # TODO: Make 56 a constant
        assert len_decoded_data >= 0x38
        decoded_data_end_idx = decoded_data_start_idx + len_decoded_data
        assert decoded_data_end_idx - 1 < len(encoded_bytes)
        return encoded_bytes[decoded_data_start_idx:decoded_data_end_idx]


def decode_to_sequence(encoded_sequence: Bytes) -> List[RLP]:
    """
    Decodes a rlp encoded byte stream assuming that the decoded data
    should be of type `Sequence` of objects.

    Parameters
    ----------
    encoded_sequence : `eth1spec.eth_types.Bytes`
        An RLP encoded Sequence.

    Returns
    -------
    decoded : `Sequence[RLP]`
        Sequence of objects decoded from `encoded_sequence`.
    """
    # TODO: Make 247 a constant
    if encoded_sequence[0] <= 0xF7:
        len_joined_encodings = encoded_sequence[0] - 192
        assert len_joined_encodings < len(encoded_sequence)
        joined_encodings = encoded_sequence[1 : 1 + len_joined_encodings]
    else:
        joined_encodings_start_idx = 1 + encoded_sequence[0] - 247
        assert joined_encodings_start_idx - 1 < len(encoded_sequence)
        # Expectation is that the big endian bytes shouldn't start with 0
        # while trying to decode using RLP, in which case is an error.
        assert encoded_sequence[1] != 0
        len_joined_encodings = Uint.from_be_bytes(
            encoded_sequence[1:joined_encodings_start_idx]
        )
        # TODO: Make 56 a constant
        assert len_joined_encodings >= 0x38
        joined_encodings_end_idx = (
            joined_encodings_start_idx + len_joined_encodings
        )
        assert joined_encodings_end_idx - 1 < len(encoded_sequence)
        joined_encodings = encoded_sequence[
            joined_encodings_start_idx:joined_encodings_end_idx
        ]

    return decode_joined_encodings(joined_encodings)


def decode_joined_encodings(joined_encodings: Bytes) -> List[RLP]:
    """
    Decodes `joined_encodings`, which is a concatenation of RLP encoded
    objects.

    Parameters
    ----------
    joined_encodings : `eth1spec.eth_types.Bytes`
        concatenation of RLP encoded objects

    Returns
    -------
    decoded : `List[RLP]`
        A list of objects decoded from `joined_encodings`.
    """
    decoded_sequence = []

    item_start_idx = 0
    while item_start_idx < len(joined_encodings):
        encoded_item_length = decode_item_length(
            joined_encodings[item_start_idx:]
        )
        assert item_start_idx + encoded_item_length - 1 < len(joined_encodings)
        encoded_item = joined_encodings[
            item_start_idx : item_start_idx + encoded_item_length
        ]
        decoded_sequence.append(decode(encoded_item))
        item_start_idx += encoded_item_length

    return decoded_sequence


def decode_item_length(encoded_data: Bytes) -> int:
    """
    Find the length of the rlp encoding for the first object in the
    encoded sequence.
    Here `encoded_data` refers to concatenation of rlp encoding for each
    item in a sequence.

    NOTE - This is a helper function not described in the spec. It was
    introduced as the spec doesn't discuss about decoding the RLP encoded
    data.

    Parameters
    ----------
    encoded_data : `eth1spec.eth_types.Bytes`
        RLP encoded data for a sequence of objects.

    Returns
    -------
    rlp_length : `int`
    """
    # Can't decode item length for empty encoding
    assert len(encoded_data) > 0

    first_rlp_byte = Uint(encoded_data[0])

    # This is the length of the big endian representation of the length of
    # rlp encoded object byte stream.
    length_length = Uint(0)
    decoded_data_length = 0

    # This occurs only when the raw_data is a single byte whose value < 128
    if first_rlp_byte < 0x80:
        # We return 1 here, as the end formula
        # 1 + length_length + decoded_data_length would be invalid for
        # this case.
        return 1
    # This occurs only when the raw_data is a byte stream with length < 56
    # and doesn't fall into the above cases
    elif first_rlp_byte <= 0xB7:
        decoded_data_length = first_rlp_byte - 128
    # This occurs only when the raw_data is a byte stream and doesn't fall
    # into the above cases
    elif first_rlp_byte <= 0xBF:
        length_length = first_rlp_byte - 183
        assert length_length < len(encoded_data)
        # Expectation is that the big endian bytes shouldn't start with 0
        # while trying to decode using RLP, in which case is an error.
        assert encoded_data[1] != 0
        decoded_data_length = Uint.from_be_bytes(
            encoded_data[1 : 1 + length_length]
        )
    # This occurs only when the raw_data is a sequence of objects with
    # length(concatenation of encoding of each object) < 56
    elif first_rlp_byte <= 0xF7:
        decoded_data_length = first_rlp_byte - 192
    # This occurs only when the raw_data is a sequence of objects and
    # doesn't fall into the above cases.
    elif first_rlp_byte <= 0xFF:
        length_length = first_rlp_byte - 247
        assert length_length < len(encoded_data)
        # Expectation is that the big endian bytes shouldn't start with 0
        # while trying to decode using RLP, in which case is an error.
        assert encoded_data[1] != 0
        decoded_data_length = Uint.from_be_bytes(
            encoded_data[1 : 1 + length_length]
        )

    return 1 + length_length + decoded_data_length
