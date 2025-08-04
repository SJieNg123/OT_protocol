import hmac
import hashlib

class PRF:
    # Initialize the PRF with a key and output length
    # The output length is optional and defaults to 32 bytes
    def __init__(self, key: bytes, output_len: int = 32):
        self.key = key
        self.output_len = output_len

    # Evaluate the PRF on an integer input x
    # The input is converted to bytes and hashed using HMAC with SHA-256
    def eval(self, x: int) -> bytes:
        x_bytes = x.to_bytes(2, 'big')  # assume N < 2^16，2 bytes is enough
        full_digest = hmac.new(self.key, x_bytes, hashlib.sha256).digest()
        return full_digest[:self.output_len]
