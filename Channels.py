import random

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