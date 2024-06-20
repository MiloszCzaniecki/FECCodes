import random

# import bchlib
# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

from Functions import *
from Channels import *
from BCH import *
from LDPC import *
import reedsolomon

import binascii
import hashlib
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TripleRepeat 
'''
from turbo.awgn import AWGN
from turbo.rsc  import RSC
from turbo.trellis import Trellis
from turbo.siso_decoder import SISODecoder
from turbo.turbo_encoder import TurboEncoder
from turbo.turbo_decoder import TurboDecoder
'''
from PIL import Image
import numpy as np
import random
import numpy as np 
import os


from PIL import Image
import numpy as np
import random
import os

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
import matplotlib.pyplot as plt
import Channels

def testuj(bity, kodowanie, dekodowanie, model,error_rate ,img = False,ilosc_powtorzen = 20 ):

            arr= [] 
            for i in range (ilosc_powtorzen):
                encoded_bits = kodowanie(bity)
                # print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))

                distorted_bits = model(encoded_bits, error_rate)
                # print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))

                decoded_bits = dekodowanie(distorted_bits)
                # print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
            
                error_count = compare_bits(bity, decoded_bits)
                if(error_count == -1 ): continue

                if(ilosc_powtorzen==1):
                    print("wchodzący  ciąg bitów:".ljust(30), bits_to_hex(bity))                    
                    print("Zakodowany ciąg bitów:".ljust(30), bits_to_hex(encoded_bits))
                    print("Zniekształcony ciąg bitów:".ljust(30),bits_to_hex(distorted_bits))
                    print("Odkodowany ciąg bitów:".ljust(30), bits_to_hex(decoded_bits))
                    print("Odkodowana wiadomość ".ljust(30), bits_to_string(decoded_bits))
                    print("Liczba różniących się bitów: ", error_count)
                arr.append( error_count/len(bity))


            return  sum(arr)/ilosc_powtorzen
            # error_enc = error_rate #encrypted 
            # error_dec = error_count / bity # decrypted 


            # if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            #     with open(file_path, "w") as file:
            #         file.write("")

            # with open(file_path, "a") as file:
            #     file.write(f"{ecc_name} {error_enc} {error_dec} \n")

            # file.close()


def png_to_bit_array(png_path):
    # Otwórz obraz PNG
    image = Image.open(png_path)
    # Przekonwertuj obraz do tablicy numpy
    image_array = np.array(image)
    # Przekonwertuj tablicę numpy do jednowymiarowego ciągu bitów
    bit_array = np.unpackbits(image)
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


def get_relative_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

def test_img(nazwa,opis,kodowanie, dekodowanie, model,error_rate ):
    input_filename = f'{nazwa}.jpg'

    output_filename = f'out/{opis}_img.png'

    # Uzyskanie ścieżek względnych
    input_path = get_relative_path(input_filename)
    output_path = get_relative_path(output_filename)

    # Konwersja PNG do ciągu bitów
    bit_array, original_shape, mode,original_image = png_to_bit_array(input_path)
    # Symulacja wprowadzenia błędów do ciągu bitów
    error_rate = 0.05 # 1% bitów będzie zmienionych
    # bit_array_with_errors  = commpy.bsc(bit_array,error_rate)

    encoded_bits = kodowanie(bit_array)
    # print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))
    distorted_bits = model(encoded_bits, error_rate)
    # print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))
    decoded_bits = dekodowanie(distorted_bits)
    # print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
    # bit_array_to_png(decoded_bits)
    # error_count = compare_bits(bity, decoded_bits)

    # bit_array_with_errors = Channels.bsc_transmission(bit_array,error_rate) 
    # bit_array_with_errors= 
    # bit_array_with_errors = introduce_errors(bit_array.copy(), error_rate)

    # Konwersja ciągu bitów z powrotem do PNG z błędami
    decoded_image = bit_array_to_png(decoded_bits, output_path, original_shape, mode)
    # fig, axs = plt.subplots(1, 2, figsize=(12, 6))


    # Oryginalny obraz
    # axs[0].imshow(original_image)
    # axs[0].set_title('Oryginalny obraz')
    # axs[0].axis('off')

    # # Zmodyfikowany obraz
    # axs[1].imshow(decoded_image)
    # axs[1].set_title('Obraz z błędami')
    # axs[1].axis('off')

    # plt.show()



def all_test():
    data_names = [" różne krótkie (8bit)","same 0 (24bit)","długie (500bit) ","długie (1000bit) "]
    data = [
        [1,0,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        np.random.randint(2, size=500),
        np.random.randint(2, size=1000) 

    ] 

    error_array = [0.01, 0.02, 0.03,0.04, 0.05 ,0.07 , 0.1, 0.13, 0.15,0.17, 0.2 ,0.23,0.25, 0.27 ,0.3, 0.33 ,0.35 ,0.37,0.4 ,0.43 ,0.45, 0.47, 0.5]
    ecc_funcs_names = ["repeat", "rs","bch", "ldpc" ]
    ecc_funcs_encodes = [TripleRepeat.triple_repeat_encode,reedsolomon.encodeRSC] # tu dopisać resztę jak będzie działać 
    ecc_funcs_decodes = [TripleRepeat.triple_repeat_decode,reedsolomon.decodeRSC]  
    file_path = "FEC_Results.txt"

    error_models_names = ["gilberta-elliota", "bsc"] 
    error_models = [gilbert_elliott_transmission,bsc_transmission]
    results = []

    for ecc_iter in range(len(ecc_funcs_encodes)):
        for model_iter in range(2):
            for error_rate in error_array:
                for i, data_type in enumerate(data_names):

                    opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
                    print("opis: "+ opis)
                    print("model iter "+ " " + str(model_iter))
                    out_err_rate = testuj(data[i], ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)
                    print("out:" + str(out_err_rate))
                    results.append({
                        'ecc_name': ecc_funcs_names[ecc_iter],
                        'model_name': error_models_names[model_iter],
                        'data_type': data_type,
                        'error_rate': error_rate,
                        'out_err_rate': out_err_rate
                    })
                # opisimg = f"nazwa_{ecc_funcs_names[ecc_iter]}_blad_wejsciowy_{error_rate}_model_kanału_{error_models_names[model_iter]}_img "
                # out_err_rate = test_img('rosesmall',opisimg, ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)



    # Konwersja wyników do DataFrame
    df = pd.DataFrame(results)

    # Generowanie wykresów
    for ecc_name in df['ecc_name'].unique():
        for model_name in df['model_name'].unique():
            for data_type in df['data_type'].unique():
                subset = df[(df['ecc_name'] == ecc_name) & (df['model_name'] == model_name) & (df['data_type'] == data_type)]
                
                plt.figure()
                plt.plot(subset['error_rate'], subset['out_err_rate'], marker='o')
                plt.title(f'ECC: {ecc_name}, Model: {model_name}, Data: {data_type}')
                plt.xlabel('Błąd wejściowy')
                plt.ylabel('Błąd wyjściowy')
                plt.grid(True)
                
                # Zapisz wykres
                filename = f'out/{ecc_name}_{model_name}_{data_type}.png'
                plt.savefig(filename)
                plt.close()
    # for ecc_iter in range(len(ecc_funcs_encodes)):
        
    #     for model_iter in range(2):
    #         for data_type in data :
    #             for error_rate in error_array:
    #                 opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
    #                 print("opis: "+ opis)
    #                 print("model iter "+ " " + str(model_iter))
    #                 out_err_rate =testuj(data_type,ecc_funcs_encodes[ecc_iter],ecc_funcs_decodes[ecc_iter],error_models[model_iter],error_rate)
    #                 # print("out:" + out_err_rate)
    #                 print(f"out: {out_err_rate}" )
    # results = []

    # for ecc_iter in range(len(ecc_funcs_encodes)):
    #     for model_iter in range(2):
    #         for data_type in data:
    #             for error_rate in error_array:
    #                 opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
    #                 print("opis: "+ opis)
    #                 print("model iter "+ " " + str(model_iter))
    #                 out_err_rate = testuj(data_type, ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)
    #                 print("out:" + str(out_err_rate))
    #                 results.append({
    #                     'ecc_name': ecc_funcs_names[ecc_iter],
    #                     'model_name': error_models_names[model_iter],
    #                     'data_type': data_type,
    #                     'error_rate': error_rate,
    #                     'out_err_rate': out_err_rate
    #                 })

    # # Konwersja wyników do DataFrame
    # df = pd.DataFrame(results)

    # # Generowanie wykresów
    # for ecc_name in df['ecc_name'].unique():
    #     for model_name in df['model_name'].unique():
    #         for data_type in df['data_type'].unique():
    #             subset = df[(df['ecc_name'] == ecc_name) & (df['model_name'] == model_name) & (df['data_type'] == data_type)]
                
    #             plt.figure()
    #             plt.plot(subset['error_rate'], subset['out_err_rate'], marker='o')
    #             plt.title(f'ECC: {ecc_name}, Model: {model_name}, Data: {data_type}')
    #             plt.xlabel('Błąd wejściowy')
    #             plt.ylabel('Błąd wyjściowy')
    #             plt.grid(True)
                
    #             # Zapisz wykres
    #             filename = f'{ecc_name}_{model_name}_{data_type}.png'
    #             plt.savefig(filename)
    #             plt.close()




data = "Przykladowy tekst."



print(string_to_bits(data))

# out_err_count=testuj(string_to_bits(data),TripleRepeat.triple_repeat_encode,TripleRepeat.triple_repeat_decode,gilbert_elliott_transmission, 0.2)
# print(f"out: {out_err_count}" )
all_test()



    



         




# interleaver = np.random.permutation(len(string_to_bits(data)))
# encoder = TurboEncoder(interleaver)
# decoder = TurboDecoder(interleaver)


# testuj(string_to_bits(data),encoder.execute,decoder.execute,gilbert_elliott_transmission)
