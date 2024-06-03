import reedsolo
from reedsolo import RSCodec, ReedSolomonError
def bytes_to_int_array(byte_data):
    """Convert a byte string to a list of integers."""
    return list(byte_data)
rsc = RSCodec(10)  # 10 ecc symbols


# przykład użycia 
encoded =  rsc.encode(b'hello')

decoded = rsc.decode(encoded)
print(decoded)


encoded =  rsc.encode([1,0,1,0,1,0,1,0,1,1,1,1,1,1])

decoded = rsc.decode(encoded)
print(bytes_to_int_array( decoded[0]))

