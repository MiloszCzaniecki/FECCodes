import random

from BCH import BCH_Init, BCH_ENCODE, BCH_DECODE
# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

from Functions import *
from Channels import *

import reedsolomon


import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import TripleRepeat
import pickle
from PIL import Image
import io


from PIL import Image


def testuj(bity, kodowanie, dekodowanie, model,error_rate ,img = False,ilosc_powtorzen = 20):
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

def test_img(nazwa, opis, kodowanie, dekodowanie, model, error_rate):
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
    data_names = [" 50bit"," 100bit"," 500bit"," 1000bit"]
    data = [
        np.random.randint(2, size=50),
        np.random.randint(2, size=100),
        np.random.randint(2, size=500),
        np.random.randint(2, size=1000) 

    ] 

    error_array = [0.01, 0.02, 0.03,0.04, 0.05 ,0.07 , 0.1, 0.13, 0.15,0.17, 0.2 ,0.23,0.25, 0.27 ,0.3, 0.33 ,0.35 ,0.37,0.4 ,0.43 ,0.45, 0.47, 0.5]
    ecc_funcs_names = ["powtórzeniowego", "rs","bch", "ldpc" ]
    ecc_funcs_encodes = [TripleRepeat.triple_repeat_encode] # tu dopisać resztę jak będzie działać 
    ecc_funcs_decodes = [TripleRepeat.triple_repeat_decode]  
    file_path = "FEC_Results.txt"

    error_models_names = ["gilberta-elliota", "bsc"] 
    error_models = [gilbert_elliott_transmission,bsc_transmission]


    results = []

    for ecc_iter in range(len(ecc_funcs_encodes)):
        for model_iter in range(2):
            for i, data_type in enumerate(data_names):
                for error_rate in error_array:
                    opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
                    print("opis: "+ opis)
                    print("model iter "+ " " + str(model_iter))
                    out_err_rates = testuj(data[i], ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)
                    avg_out_err_rate = np.mean(out_err_rates)  # Obliczamy średnią z wyników
                    print("out:" + str(out_err_rates))
                    results.append({
                        'ecc_name': ecc_funcs_names[ecc_iter],
                        'model_name': error_models_names[model_iter],
                        'data_type': data_type,
                        'error_rate': error_rate,
                        'avg_out_err_rate': avg_out_err_rate
                    })

    # Konwersja wyników do DataFrame
    df = pd.DataFrame(results)

    # Generowanie wykresów porównujących wszystkie typy danych
    for model_name in df['model_name'].unique():
        for ecc_name in df['ecc_name'].unique():
            plt.figure()
            plt.figure().set_figwidth(20)
            plt.figure().set_figheight(5)
            for data_type in df['data_type'].unique():
                subset = df[(df['ecc_name'] == ecc_name) & (df['model_name'] == model_name) & (df['data_type'] == data_type)]
                plt.plot(subset['error_rate'], subset['avg_out_err_rate'], marker='o', label=data_type)
            
            plt.title(f'Pięciokrotna zwiększenie p kodu  {ecc_name} w modelu {model_name} w zależności od błędu wejściowego',loc='center',wrap=True)
            plt.xlabel('Błąd wejściowy')
            plt.ylabel('Średni błąd wyjściowy')
            
            plt.grid(True)
            plt.legend()
            
            # Zapisz wykres
            filename = f'{ecc_name}_{model_name}_data_comparison.png'
            plt.savefig(filename)
            plt.close()




    results = []

    for ecc_iter in range(len(ecc_funcs_encodes)):
        for model_iter in range(2):
            for i, data_type in enumerate(data_names):
                for error_rate in error_array:
                    opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
                    print("opis: "+ opis)
                    print("model iter "+ " " + str(model_iter))
                    out_err_rates = testuj(data[i], ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)
                    avg_out_err_rate = np.mean(out_err_rates)  # Obliczamy średnią z wyników
                    print("out:" + str(out_err_rates))
                    results.append({
                        'ecc_name': ecc_funcs_names[ecc_iter],
                        'model_name': error_models_names[model_iter],
                        'data_type': data_type,
                        'error_rate': error_rate,
                        'avg_out_err_rate': avg_out_err_rate
                    })

    # Konwersja wyników do DataFrame
    df = pd.DataFrame(results)

    # Generowanie wykresów porównujących wszystkie metody kodowania
    for model_name in df['model_name'].unique():
        for data_type in df['data_type'].unique():
            plt.figure()
            for ecc_name in df['ecc_name'].unique():
                subset = df[(df['model_name'] == model_name) & (df['data_type'] == data_type) & (df['ecc_name'] == ecc_name)]
                plt.plot(subset['error_rate'], subset['avg_out_err_rate'], marker='o', label=ecc_name)
            
            plt.title(f'Model: {model_name}, Data: {data_type}')
            plt.xlabel('Błąd wejściowy')
            plt.ylabel('Średni błąd wyjściowy')
            plt.grid(True)
            plt.legend()
            
            # Zapisz wykres
            filename = f'{model_name}_{data_type}_comparison.png'
            plt.savefig(filename)
            plt.close()
        


    # results = []

    # for ecc_iter in range(len(ecc_funcs_encodes)):
    #     for model_iter in range(2):
    #         for error_rate in error_array:
    #             for i, data_type in enumerate(data_names):

    #                 opis = f"nazwa: {ecc_funcs_names[ecc_iter]}, błąd wejściowy : {error_rate}, model kanału : {error_models_names[model_iter]}  "
    #                 print("opis: "+ opis)
    #                 print("model iter "+ " " + str(model_iter))
    #                 out_err_rate = testuj(data[i], ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)
    #                 print("out:" + str(out_err_rate))
    #                 results.append({
    #                     'ecc_name': ecc_funcs_names[ecc_iter],
    #                     'model_name': error_models_names[model_iter],
    #                     'data_type': data_type,
    #                     'error_rate': error_rate,
    #                     'out_err_rate': out_err_rate
    #                 })
    #             # opisimg = f"nazwa_{ecc_funcs_names[ecc_iter]}_blad_wejsciowy_{error_rate}_model_kanału_{error_models_names[model_iter]}_img "
    #             # out_err_rate = test_img('rosesmall',opisimg, ecc_funcs_encodes[ecc_iter], ecc_funcs_decodes[ecc_iter], error_models[model_iter],error_rate)



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
    #             filename = f'out/{ecc_name}_{model_name}_{data_type}.png'
    #             plt.savefig(filename)
    #             plt.close()
    
# all_test()

# Wczytaj obraz z pliku
image_path = './/image//kartinka.jpg'
image = Image.open(image_path)

# Serializuj obraz do tablicy bajtów za pomocą pickle
image_byte_array = pickle.dumps(image)
bch = BCH_Init()
encodeMessage = BCH_ENCODE(bch, image_byte_array)

image_byte_array_decode = BCH_DECODE(bch,encodeMessage)


# Aby sprawdzić, możemy deserializować i wyświetlić obraz
loaded_image = pickle.loads(image_byte_array_decode)
loaded_image.show()

data = "Przykladowy tekst."



