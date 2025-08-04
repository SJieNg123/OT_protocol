import os

# xor operation on two byte strings
# Raises ValueError if lengths do not match
def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("Input lengths for xor_bytes must match.")
    return bytes(x ^ y for x, y in zip(a, b))

# Generate a random byte string of specified length
def random_bytes(length: int) -> bytes:
    return os.urandom(length)

# Convert an integer to bytes (big endian) with optional length
# If length is not specified, it will be determined based on the integer's bit length
def int_to_bytes(n: int, length: int = None) -> bytes:
    if length is None:
        length = (n.bit_length() + 7) // 8 or 1
    return n.to_bytes(length, byteorder='big')

# Convert a byte string back to an integer
def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

# Pad a byte string to a specified length (right padding with 0)
def pad_bytes(b: bytes, length: int) -> bytes:
    if len(b) > length:
        raise ValueError("Cannot pad: input is longer than target length.")
    return b.ljust(length, b'\x00')