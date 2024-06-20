import reedsolo
from reedsolo import RSCodec, ReedSolomonError
import Channels
import math
from random import random
# def bytes_to_int_array(byte_data):
#     """Convert a byte string to a list of integers."""
#     return list(byte_data)

def int_array_to_bytes(int_array):
    """Convert a list of integers to a byte string."""
    # Ensure all integers are in the range of 0-255
    byte_array = bytes(i % 256 for i in int_array)
    return byte_array
# # rsc = RSCodec(100)  # 10 ecc symbols

# def bin_to_dec(bin_matrix):
#     dec_list = []

#     for bin_list in bin_matrix:
#         temp = [str(bin_element) for bin_element in bin_list]
#         temp = ''.join(temp)
#         dec_list.append(temp)
#     return [int(number, 2) for number in dec_list]


# def dec_to_bin(lst):
#     bin_matrix = []

#     # kazda wartosc ma nowy wiersz w macierzy
#     for i in lst:
#         bin_matrix.append(list(bin(i)[2:]))

#     bin_matrix_int = [list(map(int, x)) for x in bin_matrix]
#     return bin_matrix_int



# # przykład użycia 
# # encoded =  rsc.encode(b'hello')

# # decoded = rsc.decode(encoded)
# # print(decoded)


# def encodeRSC(array_bitow):
#       nsym = max(1,len(array_bitow)//3)
#       rsc = RSCodec(  nsym) 
#       print("xdxd" ,rsc.encode(array_bitow) )
#       return bin_to_dec( rsc.encode(array_bitow))  
# def decodeRSC(array_bitow_encoded):
#     nsym = max(1, len(array_bitow_encoded)//3)
#     print(len(array_bitow_encoded))
#     print(nsym )
#     rsc = RSCodec(nsym,)
#     # bajty = int_array_to_bytes(array_bitow_encoded)
#     # decoded = rsc.decode(bajty)[0]
#     # return  bytes_to_int_array(decoded)
#     try:
#         return  bin_to_dec(rsc.decode(dec_to_bin(array_bitow_encoded))[0])
#     except:
#         # return -1
#         for i in range(len(array_bitow_encoded)):
#             array_bitow_encoded[i] = -1 
#         return array_bitow_encoded
    




# dane  = [1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0]
# # encoded =  rsc.encode()
# encoded = encodeRSC(dane )
# print("encoded  ",encoded)
# distorted = Channels.gilbert_elliott_transmission(encoded,0.01)
# print("distorted", distorted )
# # distorted = distorted[:15]
# decoded = decodeRSC(distorted)
# # decoded = rsc.decode(int_array_to_bytes ( distorted))
# print("decoded" ,decoded)
# # print(bytes_to_int_array( decoded[0]))

def bsc(input_array, p_of_error):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if random() < p_of_error:
                if input_array[i][j] == 0:
                    output_array[i][j] = 1
                else:
                    output_array[i][j] = 0
            else:
                output_array[i][j] = input_array[i][j]
    return output_array

# bsc działajacy na liście list


def bsc_lists(input_list, p_of_error):
    output_list = [[] for i in range(len(input_list))]
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if random.random() < p_of_error:
                if input_list[i][j] == 0:
                    output_list[i].append(1)
                else:
                    output_list[i].append(0)
            else:
                output_list[i].append(input_list[i][j])
    return output_list


import random
import numpy as np

import unireedsolomon
# prosty generator
def generate_bits(quantity):
    return [random.randint(0, 1) for i in range(0, quantity)]


import reedsolo
import numpy as np
import pprint


def dec_to_bin(lst):
    bin_matrix = []

    # kazda wartosc ma nowy wiersz w macierzy
    for i in lst:
        bin_matrix.append(list(bin(i)[2:]))

    bin_matrix_int = [list(map(int, x)) for x in bin_matrix]
    return bin_matrix_int


def bin_to_dec(bin_matrix):
    dec_list = []

    for bin_list in bin_matrix:
        temp = [str(bin_element) for bin_element in bin_list]
        temp = ''.join(temp)
        dec_list.append(temp)
    return [int(number, 2) for number in dec_list]


# Reed-Solomon
# ======================================================================================================================================================

# #
# print('\n===========================================================================')
# print('Kodowanie Reeda-Solomona')
lst = generate_bits(100)
print(f"Przykładowy ciąg: {lst}")

rs = unireedsolomon.rs.RSCoder(255, 223)

# potencjalnie tutaj mozna zmienic kodowanie
encoded = bytearray(rs.encode(lst), 'utf-8')

print(f"Zakodowany ciąg: {encoded}")

prepared_for_channel = dec_to_bin(list(encoded))

# print(f"Zbinaryzowany zakodowany ciąg: {prepared_for_channel}")

after_channel = bsc_lists(prepared_for_channel, 0.015)

# print(f"Zbinaryzowany ciąg po przejsciu przez kanał: {after_channel}")
# decoded = int_array_to_bytes(after_channel)
decoded = bin_to_dec(after_channel)
print(f"decoded: {decoded}")
decoded_bytearray = bytearray(decoded)

print(f"Bytearray po przejsciu przez kanal: {decoded_bytearray}")

message = rs.decode(decoded_bytearray)

print(f"Zdekodowana wiadomosc: {list(message)}")