# run.py
from src.protocol.ot_ont_out_of_n import run_ot_1outofn_protocol

if __name__ == "__main__":
    print("--- Interactive 1-out-of-N Oblivious Transfer Simulation ---")

    # 1. Get the number of messages from the user with validation
    while True:
        try:
            N_str = input("Enter the total number of messages (must be a power of 2, e.g., 4, 8, 16): ")
            N = int(N_str)
            if N > 0 and (N & (N - 1)) == 0:
                break  # Exit loop if input is valid
            else:
                print("Error: Number must be a positive power of 2.")
        except ValueError:
            print("Error: Please enter a valid integer.")

    # 2. Generate a list of dummy messages
    # All messages must have the same byte length for the protocol to work
    all_messages_str = [f"This is secret message number {i}" for i in range(N)]
    max_len = max(len(s) for s in all_messages_str)
    all_messages = [s.ljust(max_len).encode('utf-8') for s in all_messages_str]
    
    print("\nSender's database has been populated with the following messages:")
    for i, msg in enumerate(all_messages):
        print(f"  Index {i}: {msg.decode('utf-8').strip()}")
    print("-------------------------------------------------")


    # 3. Get the receiver's choice from the user with validation
    while True:
        try:
            choice_str = input(f"Enter the index of the message you want to retrieve (0 to {N-1}): ")
            receiver_choice = int(choice_str)
            if 0 <= receiver_choice < N:
                break # Exit loop if input is valid
            else:
                print(f"Error: Choice must be between 0 and {N-1}.")
        except ValueError:
            print("Error: Please enter a valid integer.")
    
    print("-------------------------------------------------")
    
    # 4. Run the protocol with the user's choices
    result = run_ot_1outofn_protocol(all_messages, receiver_choice)

    # 5. Print and verify the results
    print("\n--- Results ---")
    print(f"Receiver recovered message: '{result.decode('utf-8').strip()}'")
    print(f"Original message was:     '{all_messages[receiver_choice].decode('utf-8').strip()}'")

    if result == all_messages[receiver_choice]:
        print("\nSuccess! The recovered message is correct.")
    else:
        print("\nFailure! The recovered message is incorrect.")