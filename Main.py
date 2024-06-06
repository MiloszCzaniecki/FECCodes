import random

# import bchlib
# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

from Functions import *
from Channels import *
from BCH import *
from LDPC import *
# from RS import *

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


def testuj(bity, kodowanie, dekodowanie, model):

            print("wchodzący  ciąg bitów:".ljust(30), bits_to_hex(bity))
            encoded_bits = kodowanie(bity)
            # print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))
            print("Zakodowany ciąg bitów:".ljust(30), bits_to_hex(encoded_bits))

            distorted_bits = model(encoded_bits, error_rate=0.2)
            # print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))
            print("Zniekształcony ciąg bitów:".ljust(30),bits_to_hex(distorted_bits))

            decoded_bits = dekodowanie(distorted_bits)
            # print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
            print("Odkodowany ciąg bitów:".ljust(30), bits_to_hex(decoded_bits))

            print("Odkodowana wiadomość ".ljust(30), bits_to_string(decoded_bits))

            error_count = compare_bits(bity, decoded_bits)
            print("Liczba różniących się bitów: ", error_count)

            # error_enc = error_rate #encrypted 
            # error_dec = error_count / bity # decrypted 


            # if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            #     with open(file_path, "w") as file:
            #         file.write("")

            # with open(file_path, "a") as file:
            #     file.write(f"{ecc_name} {error_enc} {error_dec} \n")

            # file.close()



def get_ecc_name(function_name):
    return function_name.split('_')[0]

def graph(file_path):
    # odczytanie z pliku
    with open(file_path, "r") as file:
        lines = file.readlines()

    # podzielenie danych
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 0:
            ecc_name = parts[0]
            error_enc = parts[1]
            error_dec = parts[2]
            data.append([ecc_name, error_enc, error_dec])

    # organizacja danych w DataFrame
    df = pd.DataFrame(data, columns=['Operacja', 'Typ danych', 'Status'])

    # tworzenie wykresów
    for status in ['normalnego', 'ASM']:
        subset = df[(df['ECC'] == ecc_name) & (df['Po zakodowaniu '] == error_enc) & (df['Po zdekodowaniu '] == error_dec)]
        plt.plot(subset['Po zakodowaniu '], subset['Po zdekodowaniu '], label=f'{error_enc} {error_dec}')
        plt.xlabel('Błędy po zakodowaniu [%]')
        plt.ylabel('Błędy po zdekodowaniu [%]')

        plt.title(f'{ecc_name}')
        plt.legend()
        plt.savefig(f'{ecc_name}.png')
        plt.close()



# Przykład użycia
# test_BCH(string_to_byte_array(data))

# testuj(string_to_bits(data),triple_repeat_encode,triple_repeat_decode,gilbert_elliott_transmission)
#testuj(string_to_bits(data),triple_repeat_encode,triple_repeat_decode,bsc_transmission)

def all_test():
    data = [
        [1,0,0,1,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        

    ] 

    error_array = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.47, 0.5]
    ecc_funcs_names = ["bch", "ldpc", "repeat", "rs"]
    ecc_funcs_encodes = [TripleRepeat.triple_repeat_encode]
    ecc_funcs_decodes = [TripleRepeat.triple_repeat_decode]  
    file_path = "FEC_Results.txt"

    error_models_names = ["gilberta-elliota", "bsc"] 
    error_models = [gilbert_elliott_transmission,bsc_transmission]

    for model_iter in range(2):
        for data_type in data :
            for error_rate in error_array:
                for ecc_iter in range(len(ecc_funcs_encodes)):
                    opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
                    print("opis: "+ opis)
                    print("model iter "+ " " + str(model_iter))
                    testuj(data_type,ecc_funcs_encodes[ecc_iter],ecc_funcs_decodes[ecc_iter],error_models[model_iter])
                


data = "Przykladowy tekst."



print(string_to_bits(data))

testuj(string_to_bits(data),TripleRepeat.triple_repeat_encode,TripleRepeat.triple_repeat_decode,gilbert_elliott_transmission)



# all_test()



    



         




# interleaver = np.random.permutation(len(string_to_bits(data)))
# encoder = TurboEncoder(interleaver)
# decoder = TurboDecoder(interleaver)


# testuj(string_to_bits(data),encoder.execute,decoder.execute,gilbert_elliott_transmission)
