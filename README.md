# 1-out-of-N Oblivious Transfer Protocol

A Python implementation of the 1-out-of-N Oblivious Transfer (OT) cryptographic protocol based on the seminal paper **"Computationally Secure Oblivious Transfer"** by Moni Naor and Benny Pinkas. This protocol allows a receiver to retrieve one message from a database of N messages without revealing which message was selected to the sender.

## Paper Reference
This implementation is based on:
**"Computationally Secure Oblivious Transfer"**
- **Authors**: Moni Naor (Weizmann Institute), Benny Pinkas (HP Labs)
- **Published**: Journal of Cryptology, 2005 (originally appeared in CRYPTO '99)
- **DOI**: 10.1007/s00145-004-0102-6
- **Communicated by**: Joan Feigenbaum
The paper introduces efficient protocols for 1-out-of-n oblivious transfer based on the Decisional Diffie-Hellman assumption and provides the theoretical foundation for this implementation.

## Overview
Oblivious Transfer is a fundamental cryptographic primitive where:
- **Sender** has N messages: X₁, X₂, ..., Xₙ
- **Receiver** wants to retrieve message Xᵢ for some index i
- **Privacy**: Sender doesn't learn which message i was selected
- **Correctness**: Receiver only learns the selected message Xᵢ

## Protocol Description
This implementation uses the tree-based approach from the Naor-Pinkas paper that reduces 1-out-of-N OT to multiple 1-out-of-2 OT operations:

### Theoretical Foundation
The protocol is based on:
1. **Decisional Diffie-Hellman (DDH) assumption** for computational security
2. **Tree-based construction** that organizes messages in a binary tree structure
3. **Pseudorandom function families** for efficient masking

### Protocol Steps
1. **Setup Phase**: 
   - Sender generates l = log₂(N) key pairs: (K¹⁰, K¹¹), ..., (Kˡ⁰, Kˡ¹)
   - Each key pair corresponds to a level in the binary tree

2. **Masking Phase**:
   - For each message Xᵢ, compute: Yᵢ = Xᵢ ⊕ PRF(K₁^i₁, i) ⊕ ... ⊕ PRF(Kˡ^iₗ, i)
   - Where i₁i₂...iₗ is the l-bit binary representation of index i

3. **Key Exchange Phase**:
   - Receiver obtains keys corresponding to choice index via l parallel 1-out-of-2 OTs
   - This is the only interactive phase of the protocol

4. **Recovery Phase**:
   - Sender sends all masked messages {Y₁, Y₂, ..., Yₙ}
   - Receiver unmasks the desired message using obtained keys

## Project Structure
```
OT_protocol/
├── src/
│   ├── channel/
│   │   └── ot_two_one.py       # 1-out-of-2 OT channel simulation
│   ├── core/
│   │   └── prf.py              # Pseudorandom Function implementation
│   ├── protocol/
│   │   └── ot_one_out_of_n.py  # Protocol orchestration
│   ├── roles/
│   │   └── receiver.py         # OT Receiver implementation
│   │   ├── sender.py           # OT Sender implementation
│   └── utils/
│       └── bitops.py           # Bit operations and utilities
├── run.py                      # Main execution script, remove if not needed
└── README.md
```

## Requirements
- Python 3.8+
- No external dependencies (uses only standard library)

## Installation
1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd OT_protocol
   ```

## Usage
### Basic Usage
Run the protocol with predefined test messages:

```bash
python run.py
```

### Interactive Mode
The script provides an interactive mode where you can:
- Enter your own messages (number must be a power of 2)
- Choose which message index to retrieve
- See the protocol execution step by step

### Example Output

**Interactive Mode:**
```
--- Interactive 1-out-of-N Oblivious Transfer Simulation ---
Enter the total number of messages (must be a power of 2, e.g., 4, 8, 16): 4

Sender's database has been populated with the following messages:
  Index 0: This is secret message number 0
  Index 1: This is secret message number 1
  Index 2: This is secret message number 2
  Index 3: This is secret message number 3
-------------------------------------------------
Enter the index of the message you want to retrieve (0 to 3): 2
-------------------------------------------------
Sender has prepared 4 masked messages.
Receiver has obtained 2 keys via ideal OT.

--- Results ---
Receiver recovered message: 'This is secret message number 2'
Original message was:     'This is secret message number 2'

Success! The recovered message is correct.
```

**Error Handling Example:**
```
--- Interactive 1-out-of-N Oblivious Transfer Simulation ---
Enter the total number of messages (must be a power of 2, e.g., 4, 8, 16): 3
Error: Number must be a positive power of 2.
Enter the total number of messages (must be a power of 2, e.g., 4, 8, 16): 8

Sender's database has been populated with the following messages:
  Index 0: This is secret message number 0
  Index 1: This is secret message number 1
  Index 2: This is secret message number 2
  Index 3: This is secret message number 3
  Index 4: This is secret message number 4
  Index 5: This is secret message number 5
  Index 6: This is secret message number 6
  Index 7: This is secret message number 7
-------------------------------------------------
Enter the index of the message you want to retrieve (0 to 7): 10
Error: Choice must be between 0 and 7.
Enter the index of the message you want to retrieve (0 to 7): 5
-------------------------------------------------
Sender has prepared 8 masked messages.
Receiver has obtained 3 keys via ideal OT.

--- Results ---
Receiver recovered message: 'This is secret message number 5'
Original message was:     'This is secret message number 5'

Success! The recovered message is correct.
```

### Command Line Usage
You can also run the protocol with command line arguments:
```bash
python run.py "Hello" "World" "Test" "Message" 2
```
This will use the provided messages and select index 2.

## Core Components
### PRF (Pseudorandom Function)
- Located in `src/core/prf.py`
- Uses HMAC-SHA256 for secure pseudorandom generation
- Implements the PRF family required by the Naor-Pinkas construction
- Configurable output length matching message size

### OT Sender
- Located in `src/roles/sender.py`
- Implements the sender's algorithm from the paper
- Generates key pairs for the binary tree structure
- Computes masked messages using PRF evaluation

### OT Receiver
- Located in `src/roles/receiver.py`
- Implements the receiver's algorithm from the paper
- Converts choice index to binary path in the tree
- Obtains keys via OT channel simulation
- Recovers the selected message through unmasking

### OT Channel
- Located in `src/channel/ot_two_one.py`
- Simulates ideal 1-out-of-2 OT functionality
- In practice, this would use the DDH-based OT from the paper

## Implementation Notes

### Differences from Paper
- **Simplified Security Model**: Uses ideal OT simulation instead of DDH-based construction
- **Message Padding**: Requires all messages to have equal length
- **Power-of-2 Restriction**: Current implementation requires N to be a power of 2

### Cryptographic Assumptions
- In the paper: Decisional Diffie-Hellman (DDH) assumption
- In this implementation: Ideal OT channel

## Limitations
- **Simulation**: Uses ideal OT channel simulation rather than cryptographic OT
- **Message Length**: All messages must have the same length
- **Power of 2**: Number of messages must be a power of 2 (2, 4, 8, 16, ...)

## Technical Details
### Cryptographic Primitives
- **PRF**: HMAC-SHA256 based pseudorandom function family
- **XOR**: Bitwise exclusive OR for message masking
- **Binary Tree**: Organizes messages according to their binary indices

### Complexity Analysis
- **Communication**: O(log N) interactive + O(N) non-interactive
- **Computation**: O(N log N) for sender, O(log N) for receiver
- **Storage**: O(N) for sender, O(log N) for receiver
- **Rounds**: O(log N) parallel OT calls (can be done in constant rounds)

### Performance Characteristics
For N messages:
- **Key Generation**: O(log N) key pairs
- **Masking Operations**: N × log N PRF evaluations
- **OT Calls**: log N parallel 1-out-of-2 OTs
- **Message Recovery**: log N PRF evaluations + XOR operations