
import unireedsolomon
import numpy as np 


ilosc_n = 255
ilosc_k = 223




coder = unireedsolomon.RSCoder(ilosc_n,ilosc_k)
def encode (data):
    return coder.encode_fast(data)
def decode(data):
    return coder.decode(data,nostrip=False)
import struct
def int_array_to_byte_array(int_array):
    byte_array = bytearray()
    for integer in int_array:
        byte_array.extend(struct.pack('B', integer))
    return byte_array

def byte_array_to_int_array(byte_array):
    int_array = []
    for i in range(len(byte_array)):  # 1 bajt na każdą liczbę całkowitą
        integer = struct.unpack('B', byte_array[i:i+1])[0]  # 'B' dla unsigned 1-bajtowych liczb całkowitych
        int_array.append(integer)
    return int_array
import random as rand 

arr =[rand.randint(0,1) for i in range(210)]
print(arr)
print("\n\n")

def process_large_array_encode(int_array):
    bajtydodatkowe =abs( ilosc_n - (ilosc_n-ilosc_k)-(len(int_array)%ilosc_k))

    # for i in range(bajtydodatkowe):
    #     (int_array.append(0)) 
    # print("po wyrównaniu" , int_array)
    byte_array = int_array_to_byte_array(int_array)
    print(len(byte_array))
    chunk_size = ilosc_k
    processed_byte_array = bytearray()

    for i in range(0, len(byte_array), chunk_size):
        chunk = byte_array[i:i+chunk_size]
        processed_chunk = encode(chunk)
        print("processed encode",processed_chunk)
        print(len(processed_chunk))
        for c in range(ilosc_n):
            bytess = bytes(processed_chunk[c],encoding="utf-8")
            processed_byte_array.extend(bytess[0:1])

    
    processed_int_array = byte_array_to_int_array(processed_byte_array)
    return processed_int_array,bajtydodatkowe 

def process_large_array_decode(int_array, dodatkowe_bajty ):
    byte_array = int_array_to_byte_array(int_array)
    print(len(byte_array))
    chunk_size = ilosc_n
    processed_byte_array = bytearray()
    for i in range(0, len(byte_array), chunk_size):
        chunk = byte_array[i:i+chunk_size]
        processed_chunk = decode(chunk)
        for c in processed_chunk:
            try:
                processed_byte_array.extend(bytes(c, encoding='utf-8'))
            except:
                a=1
    # print("after",processed_byte_array)
    processed_int_array = byte_array_to_int_array(processed_byte_array)[0:ilosc_k]
    for i in range(dodatkowe_bajty+2):
        processed_int_array.pop()

    return processed_int_array

encoded,bajty  = process_large_array_encode(arr)
print("\n\n")
print("encoded",encoded)
print("\n\n")



decoded = process_large_array_decode(encoded,bajty )
print("zdekododwane",decoded)