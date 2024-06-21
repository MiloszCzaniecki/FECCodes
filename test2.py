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
def test_reed_solomon(data_length, num_errors):
    # Generowanie losowych danych
    data = bytearray(np.random.bytes(data_length))
    
    # Inicjalizacja kodera RS
    rs = reedsolo.RSCodec(num_errors * 2)  # Potrzebujemy 2*num_errors korekcyjnych bajtów
    
    # Kodowanie danych
    start_time = time.time()
    encoded_data = rs.encode(data)
    encode_time = time.time() - start_time
    
    # Dodanie szumu
    noisy_data = add_noise(encoded_data, num_errors)
    
    # Dekodowanie danych
    start_time = time.time()
    try:
        decoded_data = rs.decode(noisy_data)
        decode_time = time.time() - start_time
        # print(decoded_data)
        # print("\n\n\n")
        # print (data )
        success = decoded_data[0] == data
    except reedsolo.ReedSolomonError:
        decode_time = time.time() - start_time
        success = False
    
    return encode_time, decode_time, success

# Główna część programu
if __name__ == "__main__":
    data_lengths = [10000, 20000, 50000, 100000,1000000]  # Różne długości danych wejściowych
    # data_lengths = [100]  # Różne długości danych wejściowych

    num_errors = 1 # Liczba błędów do wprowadzenia
    
    for length in data_lengths:
        print(f"Testowanie dla długości danych: {length} bitów ({length//8} bajtów)")
        encode_time, decode_time, success = test_reed_solomon(length//8, length//10000)

        print(f"Czas kodowania: {encode_time:.4f} s")
        print(f"Czas dekodowania: {decode_time:.4f} s")
        print(f"Poprawność dekodowania: {'sukces' if success else 'porażka'}")
        print()