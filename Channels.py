import random

def gilbert_elliott_transmission(input_bits, error_rate):

    p_good, p_bad, p_error = 1-error_rate*5, error_rate,0.5

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

import reedsolo
import numpy as np
import time

# Funkcja do zaszumienia danych (wprowadzenie błędów)
def add_noise(data, num_errors):
    noisy_data = bytearray(data)
    indices = np.random.choice(len(data), num_errors, replace=False)
    for index in indices:
        noisy_data[index] ^= 0xFF  # Inwersja bitów w wybranych pozycjach
    return noisy_data

# Funkcja do testowania kodu RS dla różnych długości danych
# def test_reed_solomon(data_length, num_errors):
#     # Generowanie losowych danych
#     data = bytearray(np.random.bytes(data_length))
    
#     # Inicjalizacja kodera RS
#     try:
#         rs = reedsolo.RSCodec(num_errors * 2)  # Potrzebujemy 2*num_errors korekcyjnych bajtów
#     except:
#         success = False
#         return 0,0,success

#     # Kodowanie danych
#     start_time = time.time()
#     encoded_data = rs.encode(data)
#     encode_time = time.time() - start_time
    
#     # Dodanie szumu
#     noisy_data = add_noise(encoded_data, num_errors)
    
#     # Dekodowanie danych
#     start_time = time.time()
#     try:
#         decoded_data = rs.decode(noisy_data)
#         decode_time = time.time() - start_time

#         success = decoded_data[0] == data
#     except reedsolo.ReedSolomonError:
#         decode_time = time.time() - start_time
#         success = False
    
#     return encode_time, decode_time, success

# # Główna część programu
# if __name__ == "__main__":
#     data_lengths = [1000, 2000, 5000, 10000,100000]  # Różne długości danych wejściowych
#     # data_lengths = 100  # Różne długości danych wejściowych

#     num_errors = [100,200,700,1000,2000] # Liczba błędów do wprowadzenia
#     for er in num_errors:
#         for length in data_lengths:
#             # print(f"Testowanie dla długości danych: {length} bitów ({length//8} bajtów)")
#             encode_time, decode_time, success = test_reed_solomon(length//8, er)
#             # encode_time, decode_time, success = test_reed_solomon(length//8, length//10000)

#             # print(f"Czas kodowania: {encode_time:.4f} s")
#             # print(f"Czas dekodowania: {decode_time:.4f} s")
#             # print(f"Poprawność dekodowania: {'sukces' if success else 'porażka'}")

#             print(length//8 ,"bajtów/", er ,"błędów" ,f"{'sukces' if success else 'porażka'}")


def test_reed_solomon(data_length, num_errors):

    # Generowanie losowych danych
    data = bytearray(np.random.bytes(data_length))

    # Inicjalizacja kodera RS (potrzebujemy 2 * num_errors bajtów korekcyjnych)
    try:
        rs = reedsolo.RSCodec(num_errors * 2)
    except Exception as e:  # Obsługa ogólnych wyjątków
        # print(f"Błąd inicjalizacji kodera RS: {e}")
        return 0, 0, False

    # Kodowanie danych
    start_time = time.time()
    encoded_data = rs.encode(data)
    encode_time = time.time() - start_time

    # Dodanie szumu (błędów)
    noisy_data = add_noise(encoded_data, num_errors)

    # Dekodowanie danych
    start_time = time.time()
    try:
        decoded_data = rs.decode(noisy_data)
        decode_time = time.time() - start_time
        success = decoded_data[0] == data
    except reedsolo.ReedSolomonError:
        decode_time = time.time() - start_time
        success = False

    return encode_time, decode_time, success

# Główna część programu
if __name__ == "__main__":
    data_lengths = [200, 250, 500, 1000, 10000]  # Różne długości danych wejściowych
    # data_lengths = 100  # Testowanie dla jednej długości

    num_errors = [10, 20, 70, 100, 200]  # Liczba błędów do wprowadzenia

    for length in data_lengths:
        for errors in num_errors:
            encode_time, decode_time, success = test_reed_solomon(length, errors)

            print(f"{length} bajtów / {errors} błędów: {'sukces' if success else 'porażka'}")