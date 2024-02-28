from ctypes import *

# Load the shared library
libkmeans = CDLL('./libkmeans.so')  # Adjust the path as necessary

# Define the ctypes equivalent of the C structs

class Cluster(Structure):
    _fields_ = [("num_puntos", c_uint32),
                ("r", c_uint8),
                ("g", c_uint8),
                ("b", c_uint8),
                ("media_r", c_uint32),
                ("media_g", c_uint32),
                ("media_b", c_uint32)]

class RGB(Structure):
    _fields_ = [("b", c_uint8),
                ("g", c_uint8),
                ("r", c_uint8)]

class Image(Structure):
    _fields_ = [("length", c_uint32),
                ("width", c_uint32),
                ("height", c_uint32),
                ("header", c_uint8 * 54),
                ("pixels", POINTER(RGB)),
                ("fp", c_void_p)]  # FILE* is treated as void pointer

# Map the C functions
libkmeans.read_file.argtypes = [c_char_p, POINTER(Image)]
libkmeans.read_file.restype = c_int

libkmeans.write_file.argtypes = [c_char_p, POINTER(Image), POINTER(Cluster), c_uint8]
libkmeans.write_file.restype = c_int

libkmeans.getChecksum.argtypes = [POINTER(Cluster), c_uint8]
libkmeans.getChecksum.restype = c_uint32

libkmeans.find_closest_centroid.argtypes = [POINTER(RGB), POINTER(Cluster), c_uint8]
libkmeans.find_closest_centroid.restype = c_uint8

libkmeans.kmeans.argtypes = [c_uint8, POINTER(Cluster), c_uint32, POINTER(RGB)]
libkmeans.kmeans.restype = None

# Example usage
def example_usage():
    # You would need to adapt this based on how you intend to use the functions
    # and how you manage memory (especially for dynamically allocated fields like `pixels` in `Image`).
    pass

if __name__ == "__main__":
    example_usage()
