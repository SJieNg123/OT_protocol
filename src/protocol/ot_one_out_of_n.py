# channel/ot_two_one.py

class OTChannel:
    def __init__(self):
        # The channel does not need to maintain any state.
        pass

    def send(self, m0: bytes, m1: bytes, choice_bit: int) -> bytes:
        # Simulates the transfer of one of two messages.

        # Args:
        #    m0: The first message (corresponding to choice bit 0).
        #    m1: The second message (corresponding to choice bit 1).
        #    choice_bit: The receiver's choice (must be 0 or 1).

        # Returns: The message corresponding to the choice_bit.

        # Raises: ValueError: If the choice_bit is not 0 or 1.

        if choice_bit == 0:
            return m0
        elif choice_bit == 1:
            return m1
        else:
            raise ValueError("Choice bit must be 0 or 1.")