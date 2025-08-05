import os
from ..core.prf import PRF
from ..utils.bitops import int_to_bitlist, xor_bytes, random_bytes

class OTSender:
    def __init__(self, messages: list[bytes]):
        self.messages = messages  # [X1, ..., XN]
        self.N = len(messages)
        self.msg_len = len(messages[0])
        assert all(len(m) == self.msg_len for m in messages), "All messages must have the same length."

    def generate_key_pairs(self, l: int) -> list[tuple[bytes, bytes]]:
        key_pairs = []
        for _ in range(l):
            k0 = random_bytes(16)
            k1 = random_bytes(16)
            key_pairs.append((k0, k1))
        return key_pairs

    def compute_masked_messages(self, key_pairs: list[tuple[bytes, bytes]]) -> list[bytes]:
        l = len(key_pairs)
        masked = []

        for I in range(self.N):
            mask = bytes([0] * self.msg_len)
            index_bits = int_to_bitlist(I, l)  # list of bits: [i₁, i₂, ..., i_l]
            for j, bit in enumerate(index_bits):
                key = key_pairs[j][bit]
                prf = PRF(key, self.msg_len)
                mask = xor_bytes(mask, prf.eval(I))
            Y_I = xor_bytes(self.messages[I], mask)
            masked.append(Y_I)
        return masked
