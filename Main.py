import random

import bchlib
# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

import binascii
import hashlib
import os
import random



# pierwsza próbna implementacja 
# zrobiłem tak jak zrozumiałem a później przeczytałem instrukcje xdd 
# to co mi wyszło to mniej więcej BSC powielanie bitów i BER zaimplementowane 
# zaimplementowane na stringach .. bo tak w przyszłości pewnie lepiej zmienić 
# pewnie dobrze było by to zrobić z "symulacją " . 
# niewiadome o które trzeba zapytać :
# przepustowość 
# parametry transmisjii 




def string_to_bits(input_string):
    """
    Funkcja konwertująca dany ciąg znaków na ciąg bitów.
    """
    return ''.join(format(ord(char), '08b') for char in input_string)

def generate_random_bits(length, seed=None):
    """
    Funkcja generująca ciąg losowych bitów na podstawie seeda.
    """
    if seed is not None:
        random.seed(seed)
    return ''.join(str(random.randint(0, 1)) for _ in range(length))

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


    decoded = conv_decode(received, generator_matrix)
    corrected = decoded
    return corrected
def triple_repeat_encode(input_bits):
    """
    Funkcja kodująca ciąg bitów poprzez potrójne powtórzenie każdego bitu.
    """
    encoded_bits = ''
    for bit in input_bits:
        encoded_bits += bit * 3
    return encoded_bits

def triple_repeat_decode(input_bits):
    """
    Funkcja dekodująca ciąg bitów zakodowany przez potrójne powtórzenie.
    """
    decoded_bits = ''
    for i in range(0, len(input_bits), 3):
        chunk = input_bits[i:i+3]
        count_ones = chunk.count('1')
        if count_ones >= 2:
            decoded_bits += '1'
        else:
            decoded_bits += '0'
    return decoded_bits

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

def testuj(bity ,kodowanie , dekodowanie ):

    encoded_bits = kodowanie(bity)
    print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))

    distorted_bits = distort_bits(encoded_bits, error_rate=0.05)
    print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))

    decoded_bits = dekodowanie(distorted_bits)
    print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
  
    print("Odkodowana wiadomość ".ljust(40), bits_to_string(decoded_bits))

    error_count = compare_bits(bity , decoded_bits)
    print("Liczba różniących się bitów:", error_count)
        
def test_BCH(bytes):
    print(bytes)
    #predefined coder definition

    bch = bchlib.BCH(1, m=5)
    #calulate length of code words in bytes
    max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8
    #calculate chanks for enccoding decoding

    chank = len(bytes) // max_data_len;
    codestring  = bytearray()

    for i in range(chank):
        ch = bytes[i*max_data_len:(i+1)*max_data_len]
        ecc = bch.encode(ch)
        codestring = codestring + ch + ecc

    output = bytearray()
    startPositionMessage = 0;
    startPositionEcc = 0;
    endPositionMessage = 0;
    endPositionEcc = 0;

    chankForDecoding = len(codestring) // (bch.n // 8)
    for i in range(chankForDecoding):
        startPositionMessage = i*(max_data_len + ((bch.ecc_bits + 7) // 8))
        endPositionMessage = startPositionMessage + max_data_len
        startPositionEcc = endPositionMessage
        endPositionEcc = startPositionEcc + ((bch.ecc_bits + 7) // 8)

        data = codestring[startPositionMessage:endPositionMessage]
        ecc = codestring[startPositionEcc:endPositionEcc]
        bch.data_len = max_data_len
        nerr = bch.decode(data, ecc)
        bch.correct(data, ecc)
        output = output + data
    print(output)

def string_to_byte_array(input_string):
    b = bytearray()
    b.extend(map(ord, input_string))
    return b

# Przykład użycia
data = "Przykladowy tekst."
#testuj(string_to_bits(data),triple_repeat_encode,triple_repeat_decode)
test_BCH(string_to_byte_array(data))



