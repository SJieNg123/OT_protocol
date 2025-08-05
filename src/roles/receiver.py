from ..core.prf import PRF
from ..utils.bitops import int_to_bitlist, xor_bytes

class OTReceiver:
    def __init__(self, choice_index: int, l: int):
        self.choice_index = choice_index
        self.l = l
        self.choice_bits = int_to_bitlist(choice_index, l)  # I = [i₁, ..., i_l]
        self.selected_keys: list[bytes] = []

    # Obtain keys via OT
    def obtain_keys_via_ot(
        self,
        key_pairs: list[tuple[bytes, bytes]],
        channel,
    ):
        # This method simulates the OT protocol to obtain keys based on the choice bits
        self.selected_keys = []
        for j in range(self.l):
            bit = self.choice_bits[j]
            k = channel.send(key_pairs[j][0], key_pairs[j][1], bit)
            self.selected_keys.append(k)

    # Recover the message using the selected keys
    def recover_message(self, masked_db: list[bytes]) -> bytes:
        Y_I = masked_db[self.choice_index]
        mask = bytes(len(Y_I))
        for j, key in enumerate(self.selected_keys):
            prf = PRF(key, len(Y_I))
            mask = xor_bytes(mask, prf.eval(self.choice_index))
        return xor_bytes(Y_I, mask)
