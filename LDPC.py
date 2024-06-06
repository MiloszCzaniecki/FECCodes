
import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message

# n podzielne przez d_c 


n = 35
d_v = 4
d_c = 5
snr = 20
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
k = G.shape[1]
print(k)
# v = np.random.randint(2, size=k)
v = [1,1,1,1,0,1,1,1,1,1]
print(v)

y = encode(G, v, snr)

d = decode(H, y, snr)
x = get_message(G, d)
print(x)
assert abs(x - v).sum() == 0