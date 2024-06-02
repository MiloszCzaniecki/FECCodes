import bchlib


# https://github.com/jkent/python-bchlib/tree/master/.github
# import bchlib; help(bchlib)

def test_BCH(bytes):
    print(bytes)
    # predefined coder definition

    bch = bchlib.BCH(1, m=5)
    # calulate length of code words in bytes
    max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8
    # calculate chanks for enccoding decoding

    chank = len(bytes) // max_data_len;
    codestring = bytearray()

    for i in range(chank):
        ch = bytes[i * max_data_len:(i + 1) * max_data_len]
        ecc = bch.encode(ch)
        codestring = codestring + ch + ecc

    output = bytearray()
    startPositionMessage = 0;
    startPositionEcc = 0;
    endPositionMessage = 0;
    endPositionEcc = 0;

    chankForDecoding = len(codestring) // (bch.n // 8)
    for i in range(chankForDecoding):
        startPositionMessage = i * (max_data_len + ((bch.ecc_bits + 7) // 8))
        endPositionMessage = startPositionMessage + max_data_len
        startPositionEcc = endPositionMessage
        endPositionEcc = startPositionEcc + ((bch.ecc_bits + 7) // 8)

        data = codestring[startPositionMessage:endPositionMessage]
        ecc = codestring[startPositionEcc:endPositionEcc]
        bch.data_len = max_data_len
        nerr = bch.decode(data, ecc)
        bch.correct(data, ecc)
        output = output + data
    print(output)


def BCH_Init():
    return bchlib.BCH(1, m=5)


def BCH_ENCODE(bch, bytes):
    bch = bchlib.BCH(1, m=5)
    # calulate length of code words in bytes
    max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8
    # calculate chanks for enccoding decoding

    chank = len(bytes) // max_data_len;
    codestring = bytearray()

    for i in range(chank):
        ch = bytes[i * max_data_len:(i + 1) * max_data_len]
        ecc = bch.encode(ch)
        codestring = codestring + ch + ecc

    return codestring


def BCH_DECODE(bch, codestring):
    output = bytearray()
    startPositionMessage = 0;
    startPositionEcc = 0;
    endPositionMessage = 0;
    endPositionEcc = 0;

    chankForDecoding = len(codestring) // (bch.n // 8)
    max_data_len = bch.n // 8 - (bch.ecc_bits + 7) // 8

    for i in range(chankForDecoding):
        startPositionMessage = i * (max_data_len + ((bch.ecc_bits + 7) // 8))
        endPositionMessage = startPositionMessage + max_data_len
        startPositionEcc = endPositionMessage
        endPositionEcc = startPositionEcc + ((bch.ecc_bits + 7) // 8)

        data = codestring[startPositionMessage:endPositionMessage]
        ecc = codestring[startPositionEcc:endPositionEcc]
        bch.data_len = max_data_len
        nerr = bch.decode(data, ecc)
        bch.correct(data, ecc)
        output = output + data
    return output
