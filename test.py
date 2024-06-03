# import unittest
# from turbo import RSC
# from turbo import TurboEncoder
# from turbo import AWGN
# from turbo import SISODecoder
# from turbo import TurboDecoder
# import numpy as np 


# # Przykładowy interleaver
# interleaver = [2, 0, 1, 4, 3, 6, 5, 8, 7, 9]
# encoder = TurboEncoder(interleaver)
# decoder = TurboDecoder(interleaver)

# # Wiadomość o długości 1000 znaków
# message = np.random.randint(0, 2, 1000, dtype=int)

# # Rozmiar interleavera
# block_size = len(interleaver)

# # Podziel wiadomość na bloki
# num_blocks = len(message) // block_size
# if len(message) % block_size != 0:
#     num_blocks += 1

# # Zakoduj każdy blok osobno
# encoded_message = []
# for i in range(num_blocks):
#     start = i * block_size
#     end = min(start + block_size, len(message))
#     block = message[start:end]

#     # Dopełnij blok do pełnych 10 znaków, jeśli to konieczne
#     if len(block) < block_size:
#         block = np.pad(block, (0, block_size - len(block)), 'constant', constant_values=0)

#     encoded_block = encoder.execute(block)
#     encoded_message.append(encoded_block)

# # Połącz zakodowane bloki w jedną zakodowaną wiadomość
# encoded_message = np.concatenate(encoded_message)

# print("Original message:", message)
# print("Encoded message:", encoded_message)

# # Dekodowanie wiadomości
# decoded_message = []

# # Podziel zakodowaną wiadomość na bloki i dekoduj każdy z nich
# for i in range(num_blocks):
#     start = i * block_size * 3
#     end = start + block_size * 3
#     encoded_block = encoded_message[start:end]
#     decoded_block = decoder.execute(encoded_block)
#     decoded_message.append(decoded_block[:block_size])

# # Połącz zdekodowane bloki w jedną wiadomość
# decoded_message = np.concatenate(decoded_message)

# # Porównaj wyniki
# print("Decoded message:", decoded_message.astype(int))
# print("Messages are equal:", np.array_equal(message, decoded_message.astype(int)))

# def png_to_bit_array(png_path):
#     # Otwórz obraz PNG
#     image = Image.open(png_path)
#     # Przekonwertuj obraz do tablicy numpy
#     image_array = np.array(image)
#     # Przekonwertuj tablicę numpy do jednowymiarowego ciągu bitów
#     bit_array = np.unpackbits(image_array)
#     # Zwróć bit array, kształt oryginalnego obrazu i tryb
#     return bit_array, image_array.shape, image.mode

# def bit_array_to_png(bit_array, output_path, original_shape, mode='RGBA'):
#     # Przekonwertuj jednowymiarowy ciąg bitów z powrotem do tablicy numpy
#     byte_array = np.packbits(bit_array)
#     # Sprawdzenie, czy rozmiar tablicy jest zgodny z oryginalnym kształtem
#     if byte_array.size != np.prod(original_shape):
#         raise ValueError("Rozmiar bufora nie jest zgodny z oryginalnym kształtem obrazu")
#     # Zmiana kształtu tablicy do oryginalnego kształtu obrazu
#     image_array = byte_array.reshape(original_shape)
#     # Konwersja tablicy numpy z powrotem do obrazu
#     image = Image.fromarray(image_array, mode=mode)
#     # Zapis obrazu jako plik PNG
#     image.save(output_path)

# def introduce_errors(bit_array, error_rate=0.01):
#     total_bits = len(bit_array)
#     num_errors = int(total_bits * error_rate)
#     error_indices = random.sample(range(total_bits), num_errors)
#     for index in error_indices:
#         bit_array[index] = 1 - bit_array[index]  # Odwracanie bitu
#     return bit_array

# def get_relative_path(filename):
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(script_dir, filename)

# # Przykład użycia
# input_filename = 'example.png'
# output_filename = 'decoded_with_errors.png'

# # Uzyskanie ścieżek względnych
# input_path = get_relative_path(input_filename)
# output_path = get_relative_path(output_filename)

# # Konwersja PNG do ciągu bitów
# bit_array, original_shape, mode = png_to_bit_array(input_path)

# # Symulacja wprowadzenia błędów do ciągu bitów
# error_rate = 0.01  # 1% bitów będzie zmienionych
# bit_array_with_errors = introduce_errors(bit_array.copy(), error_rate)

# # Konwersja ciągu bitów z powrotem do PNG z błędami
# bit_array_to_png(bit_array_with_errors, output_path, original_shape, mode)
# # def introduce_errors(bit_array, error_rate=0.01):
# #     total_bits = len(bit_array)
# #     num_errors = int(total_bits * error_rate)
# #     error_indices = random.sample(range(total_bits), num_errors)
# #     for index in error_indices:
# #         bit_array[index] = 1 - bit_array[index]  # Odwracanie bitu
# #     return bit_array

from PIL import Image
import numpy as np
import random

import commpy
import numpy as np 
import os

import commpy.channelcoding.ldpc as ldpc
from PIL import Image
import numpy as np
import random
import os
import matplotlib.pyplot as plt
# commpy.channel 
# commpy.turbo_encoder()



def png_to_bit_array(png_path):
    # Otwórz obraz PNG
    image = Image.open(png_path)
    # Przekonwertuj obraz do tablicy numpy
    image_array = np.array(image)
    # Przekonwertuj tablicę numpy do jednowymiarowego ciągu bitów
    bit_array = np.unpackbits(image_array)
    # Zwróć bit array, kształt oryginalnego obrazu i tryb
    return bit_array, image_array.shape, image.mode, image

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
    return image 

def introduce_errors(bit_array, error_rate=0.01):
    total_bits = len(bit_array)
    num_errors = int(total_bits * error_rate)
    error_indices = random.sample(range(total_bits), num_errors)
    for index in error_indices:
        bit_array[index] = 1 - bit_array[index]  # Odwracanie bitu
    return bit_array

def get_relative_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

# Przykład użycia
# input_filename = 'purple-flower.png'
input_filename = 'rosesmall.jpg'

output_filename = 'decoded_with_errors.png'

# Uzyskanie ścieżek względnych
input_path = get_relative_path(input_filename)
output_path = get_relative_path(output_filename)

# Konwersja PNG do ciągu bitów
bit_array, original_shape, mode,original_image = png_to_bit_array(input_path)

# Symulacja wprowadzenia błędów do ciągu bitów
error_rate = 0.02 # 1% bitów będzie zmienionych
bit_array_with_errors  = commpy.bsc(bit_array,error_rate)
# bit_array_with_errors = introduce_errors(bit_array.copy(), error_rate)

# Konwersja ciągu bitów z powrotem do PNG z błędami
decoded_image = bit_array_to_png(bit_array_with_errors, output_path, original_shape, mode)
fig, axs = plt.subplots(1, 2, figsize=(12, 6))


# Oryginalny obraz
axs[0].imshow(original_image)
axs[0].set_title('Oryginalny obraz')
axs[0].axis('off')

# Zmodyfikowany obraz
axs[1].imshow(decoded_image)
axs[1].set_title('Obraz z błędami')
axs[1].axis('off')

plt.show()



# b= np.array([1,1,1,0,0,1,1,1,0])
# b, img_size,mode = png_to_bit_array(get_relative_path("purple-flower.png"))
# # a = commpy.bsc(b,0.01)
# bit_array_to_png(b,get_relative_path("output.png"),img_size,mode)

# # print(a)





# import unittest
# from turbo import RSC
# from turbo import TurboEncoder
# from turbo import AWGN
# from turbo import SISODecoder
# from turbo import TurboDecoder
# import numpy as np 

# # Przykładowy interleaver
# interleaver = [2, 0, 1, 4, 3, 6, 5, 8, 7, 9]
# encoder = TurboEncoder(interleaver)

# # Wiadomość o długości 1000 znaków
# message = np.random.randint(0, 2, 10, dtype=int)

# # Rozmiar interleavera
# block_size = len(interleaver)

# # Podziel wiadomość na bloki
# num_blocks = len(message) // block_size
# if len(message) % block_size != 0:
#     num_blocks += 1

# # Zakoduj każdy blok osobno
# encoded_message = []
# for i in range(num_blocks):
#     start = i * block_size
#     end = min(start + block_size, len(message))
#     block = message[start:end]

#     # Dopełnij blok do pełnych 10 znaków, jeśli to konieczne
#     if len(block) < block_size:
#         block = np.pad(block, (0, block_size - len(block)), 'constant', constant_values=0)

#     encoded_block = encoder.execute(block)
#     encoded_message.append(encoded_block)

# # Połącz zakodowane bloki w jedną zakodowaną wiadomość
# encoded_message = np.concatenate(encoded_message)

# print("Original message:", message)
# print("Encoded message:", encoded_message)

# decoder = TurboDecoder(interleaver)
# decoded_message = []

# # Podziel zakodowaną wiadomość na bloki i dekoduj każdy z nich
# for i in range(num_blocks):
#     start = i * block_size * 3
#     end = start + block_size * 3
#     encoded_block = encoded_message[start:end]
#     decoded_block = decoder.execute(encoded_block)
#     decoded_message.append(decoded_block[:block_size])

# # Połącz zdekodowane bloki w jedną wiadomość
# decoded_message = np.concatenate(decoded_message)

# # Porównaj wyniki
# print("Decoded message:", decoded_message)
# print("Messages are equal:", np.array_equal(message, decoded_message.astype(int)))

# class TestEncoder(unittest.TestCase):
#     # def test_rsc_encoder(self):
#     #     rsc = RSC()

#     #     input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
#     #     output_vector, _ = rsc.execute(input_vector)

#     #     print("")
#     #     print("--test_rsc_encoder--")
#     #     print("input_vector = {}".format(input_vector))
#     #     print("output_vector = {}".format(output_vector))
#     #     print("state = {}".format(rsc.registers))

#     #     self.assertListEqual(list(rsc.registers), len(rsc.registers) * [0])

#     def test_turbo_encoder(self):
#         interleaver = [8, 3, 7, 6, 9, 0, 2, 5, 1, 4]
#         turbo_encoder = TurboEncoder(interleaver)

#         input_vector = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]
#         output_vector = turbo_encoder.execute(input_vector)

#         expected_vector_1 = [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0]
#         expected_vector_2 = [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]

#         print("")
#         print("--test_turbo_encoder--")
#         print("output = {}".format(output_vector))
#         print("vec 0  = {}".format(list(output_vector[0::3])))
#         print("vec 1  = {}".format(list(output_vector[1::3])))
#         print("vec 2  = {}".format(list(output_vector[2::3])))

#         self.assertListEqual(list(output_vector[1::3]), expected_vector_1)
#         self.assertListEqual(list(output_vector[2::3]), expected_vector_2)


# class TestTurboDecoder(unittest.TestCase):
#     # def test_siso_decoder(self):
#     #     interleaver = 10 * [0]
#     #     block_size = len(interleaver) + 2

#     #     encoder = TurboEncoder(interleaver)

#     #     channel = AWGN(5)
#     #     decoder = SISODecoder(block_size)

#     #     input_vector = [0, 1, 0, 1, 1, 0, 1, 0, 0, 0]
#     #     encoded_vector = encoder.execute(input_vector)

#     #     channel_vector = list(map(float, encoded_vector))
#     #     channel_vector = channel.convert_to_symbols(channel_vector)

#     #     channel_vector = channel.execute(channel_vector)
#     #     demultiplexed_vector = decoder.demultiplex(channel_vector)

#     #     decoded_vector = decoder.execute(demultiplexed_vector)
#     #     decoded_vector = [int(b > 0.0) for b in decoded_vector]

#     #     print("")
#     #     print("--test_siso_decoder--")
#     #     print("input_vector = {}".format(input_vector))
#     #     print("encoded_vector = {}".format(encoded_vector))
#     #     print("decoded_vector = {}".format(decoded_vector))

#     #     self.assertListEqual(list(encoded_vector[::3]), decoded_vector)

#     def test_turbo_decoder(self):
#         interleaver = [9, 8, 5, 6, 2, 1, 7, 0, 3, 4]
#         encoder = TurboEncoder(interleaver)
#         decoder = TurboDecoder(interleaver)

#         channel = AWGN(20)

#         input_vector = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
#         encoded_vector = encoder.execute(input_vector)

#         channel_vector = list(map(float, encoded_vector))
#         channel_vector = channel.convert_to_symbols(channel_vector)

#         channel_vector = channel.execute(channel_vector)

#         decoded_vector = decoder.execute(channel_vector)
#         decoded_vector = [int(b > 0.0) for b in decoded_vector]

#         print("")
#         print("--test_turbo_decoder--")
#         print("input_vector = {}".format(input_vector))
#         print("encoded_vector = {}".format(encoded_vector))
#         print("decoded_vector = {}".format(decoded_vector))

#         self.assertListEqual(list(encoded_vector[::3]), decoded_vector)
# unittest.main()