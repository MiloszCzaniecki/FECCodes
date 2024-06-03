import os
from numpy import array, sqrt, zeros, zeros_like
from numpy.random import randn ,choice
from commpy.channelcoding.ldpc import get_ldpc_code_params, ldpc_bp_decode, triang_ldpc_systematic_encode
from commpy.utilities import hamming_dist

# Define the path to your LDPC design file
LDPC_DESIGN_FILE = '96.33.964.txt'

# Load LDPC code parameters
ldpc_code_params = get_ldpc_code_params(LDPC_DESIGN_FILE)

def encode_message(message_bits, ldpc_code_params):
    """
    Encodes a binary message using LDPC encoding.
    
    Parameters:
    - message_bits: Array of 0s and 1s representing the binary message
    - ldpc_code_params: LDPC code parameters loaded from the design file
    
    Returns:
    - Array of encoded bits
    """
    coded_bits = triang_ldpc_systematic_encode(message_bits, ldpc_code_params)
    return coded_bits

def decode_message(coded_bits, ldpc_code_params, decoder_algorithm='MSA', iterations=50):
    """
    Decodes an LDPC encoded binary message.
    
    Parameters:
    - coded_bits: Array of encoded bits
    - ldpc_code_params: LDPC code parameters loaded from the design file
    - decoder_algorithm: Decoding algorithm to use ('MSA' or 'SPA')
    - iterations: Number of iterations for the decoding algorithm
    
    Returns:
    - Array of decoded bits
    """
    coded_bits[coded_bits == 1] = -1
    coded_bits[coded_bits == 0] = 1
    decoded_bits, _ = ldpc_bp_decode(coded_bits.reshape(-1, order='F').astype(float), ldpc_code_params, decoder_algorithm, iterations)
    return decoded_bits

def main():
    # Example binary message
    message_bits = choice((0, 1), 40)

    print(f"Original message bits: {message_bits}")

    # Encode the message
    encoded_bits = encode_message(message_bits, ldpc_code_params)
    print(f"Encoded bits: {encoded_bits}")

    # Introduce noise (optional, for testing purposes)
    # noise_std = 0.0  # Adjust noise standard deviation as needed
    # noise = noise_std * randn(len(encoded_bits))
    # noisy_encoded_bits = encoded_bits + noise
    # noisy_encoded_bits[noisy_encoded_bits > 0] = 1
    # noisy_encoded_bits[noisy_encoded_bits <= 0] = 0

    # Decode the message
    decoded_bits = decode_message(encoded_bits, ldpc_code_params)
    decoded_message = decoded_bits[:len(message_bits)].reshape(-1, order='F')
    print(f"Decoded message bits: {decoded_message}")

    # Check if the original and decoded messages match
    if hamming_dist(message_bits, decoded_message) == 0:
        print("Success! The decoded message matches the original message.")
    else:
        print("Error: The decoded message does not match the original message.")

if __name__ == "__main__":
    main()