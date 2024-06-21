import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message

message = "sgsngfnskdlngkndskgnsdkng"
proportion = int(len(message)//11)
print(f"Dlugosc wiadomosci przed {proportion}")
k = 11
print(k)
n = int(k  *  16  /  11)
d_v = int(k * 4 / 11)
d_c = int(k * 8 / 11)

#print(f"n wynosi {n}")
#print(f"d_v wynosi {d_v}")
#print(f"d_c wynosi {d_c}")
snr = 2.0  # proporcja sygnalu do szumu
error_probability = 0.1
maxiter = 100


# Create LDPC code
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)

#print(f"Macierz parzystosci H: {H.shape}")
#print(f"Macierz generacji G: {G.shape}")

k = G.shape[1]  # Length of the message
message = np.random.randint(2, size=k)
#print(f"k wynosi {k}")
#print(f"Losowa wiadomosc: {message}")

codeword = encode(G, message, snr)

noise = np.random.normal(0, np.sqrt(1/(2*snr)), codeword.shape)
received = codeword + noise
decoded_codeword = decode(H, received, snr, maxiter)
decoded_message = get_message(G, decoded_codeword)

print(f"Wiadomosc oryginalna: {message}")
print(f"Wiadomosc zdekodowana:  {decoded_message}")
print(f"Zgodnosc:   {np.array_equal(message, decoded_message)}")
