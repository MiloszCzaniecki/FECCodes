#plik zawierajacy funkcje uzywane we wszystkich kodach korekcyjnych

import random
import bchlib
#from pyldpc import make_ldpc, encode, decode
import binascii
import hashlib
import os
import random
import numpy as np
''' uzywane typy danych:
string
bits
hex
byte
zmienne o tych typach sa zamieniane w inne'''
def generate_random_bits(length, seed=None):
    """
    Funkcja generująca ciąg losowych bitów na podstawie seeda.
    """
    if seed is not None:
        random.seed(seed)
    return ''.join(str(random.randint(0, 1)) for _ in range(length))
def compare_bits(original_bits, received_bits):
    """
    Funkcja porównująca dwa ciągi bitów i zwracająca liczbę różniących się bitów.
    """
    if(len(original_bits)!=  len(received_bits)):
        return -1
    count = 0
    for i in range(len(original_bits)):
        if original_bits[i] != received_bits[i]:
            count += 1
    return count
def distort_bits(input_bits, error_rate):
    """
    Funkcja zniekształcająca ciąg bitów zmieniając podany procent bitów na przeciwną.
    """
    distorted_bits = ''
    for bit in input_bits:
        if random.random() < error_rate:
            distorted_bits += '1' if bit == '0' else '0'

        else:
            distorted_bits += bit
    return distorted_bits

def bits_to_string(bits):
    """
    Funkcja odwracająca proces konwersji ciągu bitów na ciąg znaków.
    """
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def bits_to_hex(bits):
    """
    Funkcja konwertująca ciąg bitów na reprezentację heksadecymalną.
    """
    hex_string = hex(int(bits, 2))
    return hex_string[2:]  # Usunięcie prefiksu '0x'

def string_to_bits(input_string):
    """
    Funkcja konwertująca dany ciąg znaków na ciąg bitów.
    """
    return ''.join(format(ord(char), '08b') for char in input_string)

def string_to_byte_array(input_string):
    b = bytearray()
    b.extend(map(ord, input_string))
    return b

def bytes_to_hex(bytes):
    """
    Funkcja konwertująca bajty na reprezentację heksadecymalną.
    """
    return bytes.hex()

def bytes_to_string(bytes):
    """
    Funkcja konwertująca bahty na ciąg znaków.
    """
    return bytes.decode('utf-8')

import random



def distort_bytes(input_bytes, error_rate):
    """
    Funkcja zniekształcająca ciąg bitów zmieniając podany procent bitów na przeciwną.
    """
    distorted_bytes = bytearray()
    for byte in input_bytes:
        if random.random() < error_rate:
            if random.random() < error_rate:
                distorted_bytes.append(int.from_bytes([(byte ^ 0xFF)], 'little'))
            else:
                distorted_bytes.append(byte)
            return bytes(distorted_bytes)

def compare_bytes(original_bytes, received_bytes):
    """
    Funkcja porównująca dwa ciągi bitów i zwracająca liczbę różniących się bajtów.
    """
    if len(original_bytes) != len(received_bytes):
        return -1
    count = 0
    for i in range(len(original_bytes)):
        if original_bytes[i] != received_bytes[i]:
            count += 1
    return count