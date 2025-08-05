# run.py
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

if __name__ == "__main__":
    all_messages = [
        b'The first secret message.',
        b'This is message number 2.',
        b'The third time is a charm',
        b'Message number four here!',
    ]
    N = len(all_messages)
    receiver_choice = 3
    
    print("--- 1-out-of-N Oblivious Transfer Simulation ---")
    print(f"Sender's database contains {N} messages.")
    print(f"Receiver wants to retrieve message at index: {receiver_choice}")
    print("-------------------------------------------------")
    
    result = run_ot_1outofn_protocol(all_messages, receiver_choice)

    print("\n--- Results ---")
    print(f"Receiver recovered message: {result.decode('utf-8')}")
    print(f"Original message was:     {all_messages[receiver_choice].decode('utf-8')}")

    if result == all_messages[receiver_choice]:
        print("\n✅ Success! The recovered message is correct.")
    else:
        print("\n❌ Failure! The recovered message is incorrect.")