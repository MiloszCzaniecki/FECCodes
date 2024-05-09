import random
import pyturbo

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
    if (len(original_bits) != len(received_bits)):
        return -1
    count = 0

    for i in range(len(original_bits)):
        if original_bits[i] != received_bits[i]:
            count += 1

    return count

def bits_to_string(bits):
    """
    Funkcja odwracająca proces konwersji ciągu bitów na ciąg znaków.
    """
    binary_string = ''.join(str(bit) for bit in bits)
    bytes_list = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(byte, 2)) for byte in bytes_list)


def bits_to_hex(bits):
    """
    Funkcja konwertująca ciąg bitów na reprezentację heksadecymalną.
    """
    binary_string = ''.join(str(bit) for bit in bits)
    decimal_value = int(binary_string, 2)
    hex_string = hex(decimal_value)
    return hex_string[2:]  # Usunięcie prefiksu '0x'

def gilbert_elliott_transmission(input_bits, error_rate):
    p_good, p_bad, p_error = 1 - error_rate, error_rate, error_rate * 5

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

def bsc_transmission(input_bits, error_rate):
    p_bad = error_rate
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
        if random.random() < p_bad:
            # Zniekształcenie bitu na podstawie prawdopodobieństwa p
            output_bits.append(1 - bit)  # Flippuj bit
        else:
            output_bits.append(bit)
    return output_bits

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
        chunk = input_bits[i:i + 3]
        count_ones = chunk.count(1)
        if count_ones >= 2:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)
    return decoded_bits

def turbo_encode(input_bits):
    encoder = pyturbo.TurboEncoder(block_size=30, codebook_bits=4)
    encoded_bits = encoder.encode(input_bits)
    return encoded_bits

def turbo_decode(input_bits):
    decoder = pyturbo.TurboDecoder(block_size=30, codebook_bits=4)
    decoded_bits = decoder.decode(input_bits)
    return decoded_bits


def testuj(bity, kodowanie, dekodowanie, model, error_rate):
    print("wchodzący  ciąg bitów:".ljust(30), bits_to_hex(bity))
    encoded_bits = kodowanie(bity)
    # print("Zakodowany ciąg bitów:".ljust(40), encoded_bits,bits_to_hex( encoded_bits))
    print("Zakodowany ciąg bitów:".ljust(30), bits_to_hex(encoded_bits))

    distorted_bits = model(encoded_bits, error_rate)
    # print("Zniekształcony ciąg bitów:".ljust(40), distorted_bits,bits_to_hex( distorted_bits))
    print("Zniekształcony ciąg bitów:".ljust(30), bits_to_hex(distorted_bits))

    decoded_bits = dekodowanie(distorted_bits)
    # print("Odkodowany ciąg bitów:".ljust(40), decoded_bits,bits_to_hex( decoded_bits))
    print("Odkodowany ciąg bitów:".ljust(30), bits_to_hex(decoded_bits))

    print("Odkodowana wiadomość ".ljust(30), bits_to_string(decoded_bits))

    error_count = compare_bits(bity, decoded_bits)
    print("Liczba różniących się bitów:", error_count)


# Przykład użycia
data0 = "Przykladowy tekst"
testuj(string_to_bits(data0), triple_repeat_encode, triple_repeat_decode, gilbert_elliott_transmission, 0.1)
testuj(string_to_bits(data0), triple_repeat_encode, triple_repeat_decode, bsc_transmission, 0.7)

data1 = "NIDUC to bardzo fajny przedmiot"
testuj(string_to_bits(data1), triple_repeat_encode, triple_repeat_decode, gilbert_elliott_transmission, 0.1)
testuj(string_to_bits(data1), triple_repeat_encode, triple_repeat_decode, bsc_transmission, 0.7)




