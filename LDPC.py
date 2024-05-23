from pyldpc import make_ldpc, encode, decode, get_message
import numpy as np

message = 'Dobry denj'

n = len(message) # ilosc bitow w zakodowanej wiadomosci
#n = 15          # ilosc bitow w zakodowanej wiadomosci
d_v = 4          # stopień zmiennej
d_c = 5          # stopień sprawdzenia
snr = 100        # sygnal do poglosu, signal-to-noise ratio
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True) # macierz parzystosci i generacji
k = G.shape[1]   # bity informacyjne
v = np.random.randint(2, size=k)    # wektor dlugosci k
encoded = encode(G, v, snr)               # zakodowanie
decoded = decode(H, encoded, snr)               # zdekodowanie
x = get_message(G, decoded)               # zwraca wiadomosc zdekodowana
assert abs(x - v).sum() == 0              # porownanie z oryginalem

'''
def ldpc_encode(input_bits):
    # Calculate the length of the codeword
    n = len(input_bits)
    # Define LDPC code parameters
    d_v = 3  # Number of ones in each column of H
    d_c = 6  # Number of ones in each row of H
    # Generate LDPC parity-check matrix
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    # Encode the input bits using LDPC
    encoded_bits = encode(G, input_bits,snr=100)

    return encoded_bits

def ldpc_decode(encoded_bits):
    n = len(encoded_bits)
    # Define LDPC code parameters
    d_v = 3  # Number of ones in each column of H
    d_c = 6  # Number of ones in each row of H
    # Generate LDPC parity-check matrix
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    # Decode the encoded bits using LDPC
    decoded_bits = decode(H, encoded_bits,snr=100)
    return decoded_bits
'''
