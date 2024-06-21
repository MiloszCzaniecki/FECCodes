import numpy as np 
import random as r 

def generate_bits(quantity,random=True,value =1):
    if(random):
        return [r.random.randint(0, 1) for i in range(0, quantity)]
    return [value for i in range(0,quantity)]



# binary symmetric channel; p to prawdopodobieństwo przekłamania bitu

def bsc(input_array, p_of_error):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if r.random() < p_of_error:
                if input_array[i][j] == 0:
                    output_array[i][j] = 1
                else:
                    output_array[i][j] = 0
            else:
                output_array[i][j] = input_array[i][j]
    return output_array

# bsc działajacy na liście list


def bsc_lists(input_list, p_of_error):
    output_list = [[] for i in range(len(input_list))]
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if r.random() < p_of_error:
                if input_list[i][j] == 0:
                    output_list[i].append(1)
                else:
                    output_list[i].append(0)
            else:
                output_list[i].append(input_list[i][j])
    return output_list


# kanał Gilberta; p_of_good_to_bad to pr. przejścia ze stanu 'dobrego' do 'zlego', p_of_bad_to_good - pr. odwrotnego przejscia

def gilbert(input_array, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    good_state = True  # true oznacza stan poprawnej transmisji, false - stan przekłamań
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if good_state: # jestesmy w dobrym stanie
                if r.random() < p_of_error_when_good:
                    if input_array[i][j] == 0:
                        output_array[i][j] = 1
                    else:
                        output_array[i][j] = 0
                else:
                    output_array[i][j] = input_array[i][j]
                good_state = r.random() > p_of_good_to_bad
            else: # jestesmy w zlym stanie
                if r.random() < p_of_error_when_bad:
                    if input_array[i][j] == 0:
                        output_array[i][j] = 1
                    else:
                        output_array[i][j] = 0
                else:
                    output_array[i][j] = input_array[i][j]
                good_state = r.random() > (1 - p_of_bad_to_good)
    return output_array

# kanał gilberta działający na liście list
def gilbert_lists(input_list, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good):
    output_list = [[] for i in range(len(input_list))]
    good_state = True  # true oznacza stan poprawnej transmisji, false - stan przekłamań
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if good_state: # jestesmy w dobrym stanie
                if r.random() < p_of_error_when_good:
                    if input_list[i][j] == 0:
                        output_list[i].append(1)
                    else:
                        output_list[i].append(0)
                else:
                    output_list[i].append(input_list[i][j])
                good_state = r.random() > p_of_good_to_bad
            else: # jestesmy w zlym stanie
                if r.random() < p_of_error_when_bad:
                    if input_list[i][j] == 0:
                        output_list[i].append(1)
                    else:
                        output_list[i].append(0)
                else:
                    output_list[i].append(input_list[i][j])
                good_state = r.random() > (1 - p_of_bad_to_good)
    return output_list


def calculate_gilbert_elliott_error(p_error_good, p_good_to_bad, p_error_bad, p_bad_to_good):
    # Obliczanie długookresowych prawdopodobieństw stanów
    pi_G = p_bad_to_good / (p_good_to_bad + p_bad_to_good)
    pi_B = p_good_to_bad / (p_good_to_bad + p_bad_to_good)
    
    # Obliczanie średniego prawdopodobieństwa błędu
    p_error = pi_G * p_error_good + pi_B * p_error_bad
    
    return p_error

# Przykładowe wartości parametrów
p_error_good = 0.001
p_good_to_bad = 0.1
p_error_bad = 1
p_bad_to_good = 0.5

# Obliczanie średniego prawdopodobieństwa błędu
average_error_probability = calculate_gilbert_elliott_error(p_error_good, p_good_to_bad, p_error_bad, p_bad_to_good)

print("Średnie prawdopodobieństwo błędu w kanale Gilbert-Elliott:", average_error_probability)

from numpy import array
listain = generate_bits(100,False,1)
print("gilbert-elliot channel")
print("in " , "".join(str(i) for i in  listain))
out = gilbert(array([[i for i in listain]]), 0.001, 0.1, 1, 0.5)
# print(f"out { out}")
print(f"out { ''.join(str(i) for i in  out[0])}")

print("bsc")
listain = generate_bits(100,False,1)
print("in " , "".join(str(i) for i in  listain))
out = bsc(array([[i for i in listain]]), 0.1675)
print(f"out { ''.join(str(i) for i in  out[0])}")
def count_repeated_zeros(sequence, max_repeats=30):
    counts = np.zeros(max_repeats + 1, dtype=int)
    count = 0
    
    for bit in sequence:
        if bit == 0:
            count += 1
        else:
            if count > 0:
                counts[min(count, max_repeats)] += 1
            count = 0
    if count > 0:
        counts[min(count, max_repeats)] += 1
    
    return counts

def print_counts(counts):
    for i, count in enumerate(counts):
        if count > 0:
            print(f"{i}-krotne powtórzenie: {count} razy")


maxpowtorzonychzer = 30
gilbert_counts = [0]*maxpowtorzonychzer
bsc_counts = [0]*maxpowtorzonychzer 
ilosc_powtorzen  = 10000

for i in range(ilosc_powtorzen):
    listain = generate_bits(1000, False, 1)
    # print("gilbert-elliot channel")
    # print("in", "".join(str(i) for i in listain))
    out = gilbert(array([[i for i in listain]]), 0.001, 0.2, 1, 0.5)
    # print(f"out {''.join(str(i) for i in out[0])}")

    gilbert_counts_tmp = count_repeated_zeros(out[0])
    # print(i)
    


    # print("bsc")
    listain = generate_bits(1000, False, 1)
    # print("in", "".join(str(i) for i in listain))
    out = bsc(array([[i for i in listain]]), 0.1675)
    # print(f"out {''.join(str(i) for i in out[0])}")

    bsc_counts_tmp = count_repeated_zeros(out[0])
    for j in range(maxpowtorzonychzer):
        gilbert_counts[j] +=gilbert_counts_tmp[j]
        bsc_counts[j]+=bsc_counts_tmp[j]

print("Powtórzenia zer w kanale gilbert-elliot:")
print_counts(gilbert_counts)
print(f"wszystkich zmian :{sum(gilbert_counts)}")

print("Powtórzenia zer w kanale bsc:")
print_counts(bsc_counts)
print(f"wszystkich zmian :{sum(bsc_counts)}")
