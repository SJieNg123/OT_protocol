import math
from src.roles.sender import OTSender
from src.roles.receiver import OTReceiver
from src.channel.ot_two_one import OTChannel

def run_ot_1outofn_protocol(messages: list[bytes], choice_index: int) -> bytes:
    N = len(messages)
    assert N > 0 and (N & (N - 1)) == 0, "Number of messages must be a power of 2."
    l = int(math.log2(N))

    sender = OTSender(messages)
    key_pairs = sender.generate_key_pairs(l)
    masked_db = sender.compute_masked_messages(key_pairs)
    print(f"Sender has prepared {N} masked messages.")

    channel = OTChannel()
    receiver = OTReceiver(choice_index, l)
    receiver.obtain_keys_via_ot(key_pairs, channel)
    print(f"Receiver has obtained {len(receiver.selected_keys)} keys via ideal OT.")

    recovered_message = receiver.recover_message(masked_db)
    return recovered_message
