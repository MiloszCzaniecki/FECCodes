import numpy as np
from scipy.sparse import csc_matrix
from commpy.channelcoding.ldpc import triang_ldpc_systematic_encode,ldpc_bp_decode 


# Funkcja pomocnicza do budowania macierzy generatora i sprawdzającej parzystość
def build_matrix(ldpc_code_params):
    n_vnodes = ldpc_code_params['n_vnodes']
    n_cnodes = ldpc_code_params['n_cnodes']

    # Przykladowe dane dla macierzy sprawdzającej parzystość
    H_data = np.array([
        [1, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 1]
    ], dtype=np.int8)
    
    # Konwersja do formatu rzadkiego CSC
    ldpc_code_params['parity_check_matrix'] = csc_matrix(H_data)

    # Macierz generatora musi być obliczona z macierzy sprawdzającej parzystość
    # W tym przykładzie jest to macierz jednostkowa o odpowiednich wymiarach
    G_data = np.eye(n_vnodes, dtype=np.int8)
    ldpc_code_params['generator_matrix'] = G_data

def triang_ldpc_systematic_encode(message_bits, ldpc_code_params, pad=True):
    if ldpc_code_params.get('generator_matrix') is None or ldpc_code_params.get('parity_check_matrix') is None:
        build_matrix(ldpc_code_params)

    block_length = ldpc_code_params['generator_matrix'].shape[1]
    modulo = len(message_bits) % block_length
    if modulo:
        if pad:
            message_bits = np.concatenate((message_bits, np.zeros(block_length - modulo, message_bits.dtype)))
        else:
            raise ValueError('Padding is disable but message length is not a multiple of block length.')
    message_bits = message_bits.reshape(-1, block_length, order='F')

    parity_part = ldpc_code_params['generator_matrix'].dot(message_bits.T).T % 2
    return np.hstack((message_bits, parity_part)).astype(np.int8)

def ldpc_bp_decode(llr_vec, ldpc_code_params, decoder_algorithm, n_iters):
    llr_vec.clip(-500, 500, llr_vec)
    if ldpc_code_params.get('parity_check_matrix') is None:
        build_matrix(ldpc_code_params)

    dec_word = np.sign(llr_vec).astype(np.int8)
    out_llrs = llr_vec.copy()
    parity_check_matrix = ldpc_code_params['parity_check_matrix'].astype(float).tocoo()

    for i_start in range(0, llr_vec.size, ldpc_code_params['n_vnodes']):
        i_stop = i_start + ldpc_code_params['n_vnodes']
        message_matrix = parity_check_matrix.multiply(llr_vec[i_start:i_stop])

        for iter_cnt in range(n_iters):
            if np.all(ldpc_code_params['parity_check_matrix'].multiply(dec_word[i_start:i_stop]).sum(1) % 2 == 0):
                break

            if decoder_algorithm == 'SPA':
                message_matrix.data *= .5
                np.tanh(message_matrix.data, out=message_matrix.data)

                with np.errstate(divide='ignore', invalid='ignore'):
                    log2_msg_matrix = message_matrix.astype(complex).copy()
                    np.log2(message_matrix.data.astype(complex), out=log2_msg_matrix.data)
                    msg_products = np.exp2(log2_msg_matrix.sum(1)).real

                    message_matrix.data = 1 / message_matrix.data
                    message_matrix = message_matrix.multiply(msg_products)
                    message_matrix.data.clip(-1, 1, message_matrix.data)
                    np.arctanh(message_matrix.data, out=message_matrix.data)
                    message_matrix.data *= 2
                    message_matrix.data.clip(-500, 500, message_matrix.data)

            elif decoder_algorithm == 'MSA':
                message_matrix = message_matrix.tocsr()
                for row_idx in range(message_matrix.shape[0]):
                    begin_row = message_matrix.indptr[row_idx]
                    end_row = message_matrix.indptr[row_idx + 1]
                    row_data = message_matrix.data[begin_row:end_row].copy()
                    indexes = np.arange(len(row_data))
                    for j, i in enumerate(range(begin_row, end_row)):
                        other_val = row_data[indexes != j]
                        message_matrix.data[i] = np.sign(other_val).prod() * np.abs(other_val).min()
            else:
                raise NameError('Please input a valid decoder_algorithm string (meaning "SPA" or "MSA").')

            msg_sum = np.array(message_matrix.sum(0)).squeeze()
            message_matrix.data *= -1
            message_matrix.data += parity_check_matrix.multiply(msg_sum + llr_vec[i_start:i_stop]).data

            out_llrs[i_start:i_stop] = msg_sum + llr_vec[i_start:i_stop]
            np.signbit(out_llrs[i_start:i_stop], out=dec_word[i_start:i_stop])

    n_blocks = llr_vec.size // ldpc_code_params['n_vnodes']
    dec_word = dec_word.reshape(-1, n_blocks, order='F').squeeze().astype(np.int8)
    out_llrs = out_llrs.reshape(-1, n_blocks, order='F').squeeze()
    return dec_word, out_llrs

# Przykladowa wiadomość do zakodowania (dowolna długość)
input_string = "Hello, LDPC coding!"
message_bits = np.unpackbits(np.frombuffer(input_string.encode(), dtype=np.uint8))

# Przykladowe parametry LDPC
ldpc_code_params = {
    'n_vnodes': 7,
    'n_cnodes': 4,
    'max_cnode_deg': 3,
    'cnode_adj_list': np.array([0, 2, 3, 1, 2, 4, 0, 1, 5, 2, 5, 6]),
    'cnode_deg_list': np.array([3, 3, 3, 3])
}

# Budowanie macierzy generatora i sprawdzającej parzystość
build_matrix(ldpc_code_params)

# Kodowanie wiadomości
coded_message = triang_ldpc_systematic_encode(message_bits, ldpc_code_params)

print("Zakodowana wiadomość:", coded_message)

# Symulowanie odbioru wiadomości przez kanał szumowy (BPSK z szumem Gaussowskim)
# llr_vec = 2 * coded_message - 1  # BPSK: 0 -> -1, 1 -> 1
# llr_vec = llr_vec + 0.5 * np.random.randn(len(coded_message))  # Dodanie szumu

# Dekodowanie wiadomości
decoded_bits, out_llrs = ldpc_bp_decode(coded_message, ldpc_code_params, 'SPA', 50)

# Odkodowanie wiadomości z bitów
decoded_bytes = np.packbits(decoded_bits)[:len(input_string)]
decoded_string = decoded_bytes.tobytes().decode()

print("Odebrane bity:", np.round(llr_vec))
print("Dekodowane bity:", decoded_bits)
print("Odkodowana wiadomość:", decoded_string)