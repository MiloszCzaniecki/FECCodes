import random
import numpy #as np

#from pyldpc import make_ldpc, encode, decode

import binascii
import hashlib
import os
import random


from Functions import *     # Functions -> zawiera funkcje typu zamiany stringi na bajty itd.
from RS import *            # RS 
from Repeat import *        # Potrójnie powtórzony kod 
from LDPC import *          # LDPC
from BCH import *           # BCH

# każda używana biblioteka jest unikatowa dlatego testy będą musiały być różnie przeprowadzane dla różnych FEC

def test(bity ,kodowanie , dekodowanie):

    encoded_bits = kodowanie(bity)
    print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))

    distorted_bits = distort_bits(encoded_bits, error_rate=0.05)
    print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))

    decoded_bits = dekodowanie(distorted_bits)
    print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
  
    print("Odkodowana wiadomość ".ljust(40), bits_to_string(decoded_bits))

    error_count = compare_bits(bity , decoded_bits)
    print("Liczba różniących się bitów:", error_count)
        


# Przykład użycia
data0 = "Przykladowy tekst."
#test(string_to_bits(data0),triple_repeat_encode,triple_repeat_decode)
#test(string_to_bits(data0),ldpc_encode,ldpc_decode)
#test_BCH(string_to_byte_array(data0))






