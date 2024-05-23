# https://pypi.org/project/reedsolo/
# biblioteka dziala na BAJTACH
import gen
import reedsolo as rs
from reedsolo import *
from Functions import *
from reedsolo import RSCodec, ReedSolomonError

rsc = RSCodec(10)  # 10 ecc symbols

message = 'Siema '
encoded_bytes = rsc.encode([1,2,3,4]) #dziala tylko dla tych konkretnych liczb
#encoded_bytes = rsc.encode(message) nie działa

tampered_msg = b'heXlo worXd\xed%T\xc4\xfdX\x89\xf3\xa8\xaa'
distorted_bytes = distort_bytes(encoded_bytes, 0.1)
decoded_bytes, decoded_msgecc, errata_pos = rsc.decode(distorted_bytes)
error_count = compare_bytes(encoded_bytes, decoded_bytes)

print("Zakodowany ciąg bitów:".ljust(40), encoded_bytes, bytes_to_hex(encoded_bytes))

print("Zniekształcony ciąg bitów:".ljust(40), distorted_bytes, bytes_to_hex(distorted_bytes))

print("Odkodowany ciąg bitów:".ljust(40), decoded_bytes, bytes_to_hex(decoded_bytes))

print("Liczba różniących się bitów:", error_count)
'''

print("Poprawiona wiadomość ".ljust(40), bytes_to_string(corrected_bytes))

#'''