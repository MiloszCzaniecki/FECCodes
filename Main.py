import random

# import bchlib
# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

import binascii
import hashlib
import os
import random
import numpy as np
from turbo.awgn import AWGN
from turbo.rsc  import RSC
from turbo.trellis import Trellis
from turbo.siso_decoder import SISODecoder
from turbo.turbo_encoder import TurboEncoder
from turbo.turbo_decoder import TurboDecoder
from PIL import Image
import numpy as np
import random

import commpy
import numpy as np 
import os


from PIL import Image
import numpy as np
import random
import os





def string_to_bits(input_string):
    """
    Funkcja konwertująca dany ciąg znaków na ciąg bitów.
    """
    return [int(bit) for char in input_string for bit in format(ord(char), '08b')]

def generate_random_bits(length, seed=None):
    """
    Funkcja generująca ciąg losowych bitów na podstawie seeda.
    """
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, 1) for _ in range(length)]



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
def gilbert_elliott_transmission(input_bits, error_rate):

    p_good, p_bad, p_error = 1-error_rate, error_rate,error_rate*5

    """
    Symuluje działanie modelu Gilberta-Elliotta.

    Args:
        input_bits (list): Lista zawierająca bity wejściowe (0 lub 1).
        p_good (float): Prawdopodobieństwo przejścia do stanu dobrego.
        p_bad (float): Prawdopodobieństwo przejścia do stanu złego.
        p_error (float): Prawdopodobieństwo zniekształcenia bitu w stanie złym.

    Returns:
        list: Lista zawierająca bity wyjściowe po transmisji.
    """
    state_good = True  # Początkowy stan kanału: dobry
    output_bits = []

    for bit in input_bits:
        if state_good:
            if random.random() < p_bad:
                state_good = False
        else:
            if random.random() < p_good:
                state_good = True

        if state_good:
            output_bits.append(bit)
        else:
            if random.random() < p_error:
                output_bits.append(1 - bit)  # Flippuj bit
            else:
                output_bits.append(bit)

    return output_bits
def bsc_transmission(input_bits,error_rate ):
    p = error_rate
    """
    Symuluje działanie modelu BSC (Binary Symmetric Channel).

    Args:
        input_bits (list): Lista zawierająca bity wejściowe (0 lub 1).
        p (float): Prawdopodobieństwo zniekształcenia bitu.

    Returns:
        list: Lista zawierająca bity wyjściowe po transmisji.
    """
    output_bits = []
    for bit in input_bits:
        if random.random() < p:
            # Zniekształcenie bitu na podstawie prawdopodobieństwa p
            output_bits.append(1 - bit)  # Flippuj bit
        else:
            output_bits.append(bit)
    return output_bits


    decoded = conv_decode(received, generator_matrix)
    corrected = decoded
    return corrected
def triple_repeat_encode(input_bits):
    """
    Funkcja kodująca ciąg bitów poprzez potrójne powtórzenie każdego bitu.
    """
    encoded_bits = []
    for bit in input_bits:
        encoded_bits.append(bit) 
        encoded_bits.append(bit)
        encoded_bits.append(bit)

        # encoded_bits += bit * 3
    return encoded_bits

def triple_repeat_decode(input_bits):
    """
    Funkcja dekodująca ciąg bitów zakodowany przez potrójne powtórzenie.
    """
    decoded_bits = []
    for i in range(0, len(input_bits), 3):
        chunk = input_bits[i:i+3]
        count_ones = chunk.count(1)
        if count_ones >= 2:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)
    return decoded_bits

def bits_to_string(bits):
    """
    Funkcja odwracająca proces konwersji ciągu bitów na ciąg znaków.
    """
    binary_string = ''.join(str(bit) for bit in bits)
    bytes_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(byte, 2)) for byte in bytes_list)

def png_to_bit_array(png_path):
    # Otwórz obraz PNG
    image = Image.open(png_path)
    # Przekonwertuj obraz do tablicy numpy
    image_array = np.array(image)
    # Przekonwertuj tablicę numpy do jednowymiarowego ciągu bitów
    bit_array = np.unpackbits(image_array)
    # Zwróć bit array, kształt oryginalnego obrazu i tryb
    return bit_array, image_array.shape, image.mode

def bit_array_to_png(bit_array, output_path, original_shape, mode='RGBA'):
    # Przekonwertuj jednowymiarowy ciąg bitów z powrotem do tablicy numpy
    byte_array = np.packbits(bit_array)
    # Debugowanie rozmiarów
    print(f'Expected byte size: {np.prod(original_shape)}')
    print(f'Actual byte size: {byte_array.size}')
    # Sprawdzenie, czy rozmiar tablicy jest zgodny z oryginalnym kształtem
    if byte_array.size != np.prod(original_shape):
        raise ValueError("Rozmiar bufora nie jest zgodny z oryginalnym kształtem obrazu")
    # Zmiana kształtu tablicy do oryginalnego kształtu obrazu
    image_array = byte_array.reshape(original_shape)
    # Konwersja tablicy numpy z powrotem do obrazu
    image = Image.fromarray(image_array, mode=mode)
    # Zapis obrazu jako plik PNG
    image.save(output_path)



def bits_to_hex(bits):
    """
    Funkcja konwertująca ciąg bitów na reprezentację heksadecymalną.
    """
    binary_string = ''.join(str(bit) for bit in bits)
    decimal_value = int(binary_string, 2)
    hex_string = hex(decimal_value)
    return hex_string[2:]  # Usunięcie prefiksu '0x'
def testuj(bity ,kodowanie , dekodowanie,model  ):



    print("wchodzący  ciąg bitów:".ljust(30), bits_to_hex( bity))
    encoded_bits = kodowanie(bity)
    # print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))
    print("Zakodowany ciąg bitów:".ljust(30), bits_to_hex( encoded_bits))

    distorted_bits = model(encoded_bits, error_rate=0.2)
    # print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))
    print("Zniekształcony ciąg bitów:".ljust(30),bits_to_hex( distorted_bits))

    decoded_bits = dekodowanie(distorted_bits)
    # print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
    print("Odkodowany ciąg bitów:".ljust(30), bits_to_hex( decoded_bits))
  
    print("Odkodowana wiadomość ".ljust(30), bits_to_string(decoded_bits))

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
    startPositionMessage = 0
    startPositionEcc = 0
    endPositionMessage = 0
    endPositionEcc = 0

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
# test_BCH(string_to_byte_array(data))

# testuj(string_to_bits(data),triple_repeat_encode,triple_repeat_decode,gilbert_elliott_transmission)
#testuj(string_to_bits(data),triple_repeat_encode,triple_repeat_decode,bsc_transmission)



interleaver = np.random.permutation(len(string_to_bits(data)))
encoder = TurboEncoder(interleaver)
decoder = TurboDecoder(interleaver)


testuj(string_to_bits(data),encoder.execute,decoder.execute,gilbert_elliott_transmission)
