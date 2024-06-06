# def triple_repeat_encode(input_bits):
#     """
#     Funkcja kodująca ciąg bitów poprzez potrójne powtórzenie każdego bitu.
#     """
#     encoded_bits = ''
#     for bit in input_bits:
#         encoded_bits += bit * 3
#     return encoded_bits

# def triple_repeat_decode(input_bits):
#     """
#     Funkcja dekodująca ciąg bitów zakodowany przez potrójne powtórzenie.
#     """
#     decoded_bits = ''
#     for i in range(0, len(input_bits), 3):
#         chunk = input_bits[i:i+3]
#         count_ones = chunk.count('1')
#         if count_ones >= 2:
#             decoded_bits += '1'
#         else:
#             decoded_bits += '0'
#     return decoded_bits

def triple_repeat_encode(input_bits):
    """
    Funkcja kodująca tablicę bitów poprzez potrójne powtórzenie każdego bitu.
    """
    encoded_bits = []
    for bit in input_bits:
        encoded_bits.extend([bit] * 3)
    return encoded_bits

def triple_repeat_decode(input_bits):
    """
    Funkcja dekodująca tablicę bitów zakodowaną przez potrójne powtórzenie.
    """
    if len(input_bits) % 3 != 0:
        raise ValueError("Długość tablicy bitów musi być wielokrotnością 3.")
    
    decoded_bits = []
    for i in range(0, len(input_bits), 3):
        chunk = input_bits[i:i+3]
        count_ones = chunk.count(1)
        if count_ones >= 2:
            decoded_bits.append(1)
        else:
            decoded_bits.append(0)
    return decoded_bits