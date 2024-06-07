import reedsolo
from reedsolo import RSCodec, ReedSolomonError
import Channels
import math
def bytes_to_int_array(byte_data):
    """Convert a byte string to a list of integers."""
    return list(byte_data)

def int_array_to_bytes(int_array):
    """Convert a list of integers to a byte string."""
    # Ensure all integers are in the range of 0-255
    byte_array = bytes(i % 256 for i in int_array)
    return byte_array
# rsc = RSCodec(100)  # 10 ecc symbols


# przykład użycia 
# encoded =  rsc.encode(b'hello')

# decoded = rsc.decode(encoded)
# print(decoded)


def encodeRSC(array_bitow):
      nsym = max(1,len(array_bitow)//10)
      rsc = RSCodec(  nsym) 
      return bytes_to_int_array( rsc.encode(array_bitow))  
def decodeRSC(array_bitow_encoded):
    nsym = max(1, len(array_bitow_encoded)//11)
    print(len(array_bitow_encoded))
    print(nsym )
    rsc = RSCodec(nsym,)
    # bajty = int_array_to_bytes(array_bitow_encoded)
    # decoded = rsc.decode(bajty)[0]
    # return  bytes_to_int_array(decoded)


    try:
        return  bytes_to_int_array(rsc.decode(int_array_to_bytes(array_bitow_encoded))[0])
    except:
        for i in range(len(array_bitow_encoded)):
            array_bitow_encoded[i] = -1 
        return array_bitow_encoded

# dane  = [1,0,1,0,1,0,1,0,1,1,1,1,1,1]
# # encoded =  rsc.encode()
# encoded = encodeRSC(dane )
# print("encoded  ",encoded)
# distorted = Channels.gilbert_elliott_transmission(encoded,0.1)
# print("distorted", distorted )
# # distorted = distorted[:15]
# decoded = decodeRSC(int_array_to_bytes( distorted))
# # decoded = rsc.decode(int_array_to_bytes ( distorted))
# print("decoded" ,decoded)
# print(bytes_to_int_array( decoded[0]))

