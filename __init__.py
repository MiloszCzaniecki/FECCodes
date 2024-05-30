#
# Simple Turbo Codes Implementation
#
import numpy as np
from turbo.awgn import AWGN
from turbo.rsc  import RSC
from turbo.trellis import Trellis
from turbo.siso_decoder import SISODecoder
from turbo.turbo_encoder import TurboEncoder
from turbo.turbo_decoder import TurboDecoder


import numpy as np


interleaver = [9, 8, 5, 6, 2, 1, 7, 0, 3, 4]
encoder = TurboEncoder(interleaver)
decoder = TurboDecoder(interleaver)

channel = AWGN(500)

input_vector = [1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
encoded_vector = encoder.execute(input_vector)

channel_vector = list(map(float, encoded_vector))
channel_vector = channel.convert_to_symbols(channel_vector)

channel_vector = channel.execute(channel_vector)

decoded_vector = decoder.execute(channel_vector)
decoded_vector = [int(b > 0.0) for b in decoded_vector]

print("")
print("--test_turbo_decoder--")
print("input_vector = {}".format(input_vector))
print("encoded_vector = {}".format(encoded_vector))
print("decoded_vector = {}".format(decoded_vector))
