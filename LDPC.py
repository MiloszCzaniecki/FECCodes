import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message
import math

def ldpc_encode(message, snr, d_v=4, d_c=5):
    # Calculate n and k based on the message length
    k = len(message)

    n = max(d_v, d_c)
    while n % d_v != 0 or n % d_c != 0 or n < k:
        n += 1
    # Generate the LDPC code
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    print("Ksztalt macierzy parzystosci H:", H.shape)
    print("Ksztalt macierzy generacji G:", G.shape)

    padded_message = np.pad(message, (0, n - k), 'constant')
    #transponowanie macierzy
    G = G.T

    # Encode the message
    encoded_message = encode(G, padded_message, snr)
    return encoded_message


def ldpc_decode(received_message, snr, d_v=4, d_c=5):
    # Calculate n and k based on the received message length
    n = len(received_message)
    k = n - (n // d_v) * d_v

    # Generate the LDPC code
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)

    # Decode the received message
    decoded_message = decode(H, received_message, snr, maxiter=100, log=True)
    return decoded_message


# Example usage:
message = np.random.randint(2, size=520)  # 512-bit message
snr = 10
encoded_message = ldpc_encode(message, snr)
received_message = encoded_message # + np.random.randint(2, size=len(encoded_message))  # Add some noise
decoded_message = ldpc_decode(received_message, snr)

print("Original message: ", message)
print("Decoded message: ", decoded_message)