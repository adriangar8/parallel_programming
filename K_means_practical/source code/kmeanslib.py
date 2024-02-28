'''
This script is a Python module that demonstrates how to use the kmeans 
C library in Python using ctypes.
'''

from ctypes import *

# Import a shared library called "libkmeans.so" using the CDLL class from the ctypes module in Python.
libkmeans = CDLL('/home/agarcias/Documents/UAB_year3/parallel_programming/parallel_programming_repo/K_means_practical/source code/libkmeans.so') 

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

def example_usage():

    image_path = b'imagen.bmp'  # Path to the input BMP image
    output_image_path = b'output_img.bmp'  # Path for the output BMP image

    # Instantiate the Image structure
    img = Image()

    # Read the image file
    if libkmeans.read_file(image_path, byref(img)) == -1:
        print("Failed to read the image")
        return

    # Define the number of clusters and instantiate Cluster array
    k = 3  # Number of clusters
    centroids = (Cluster * k)()

    # Initialize centroids (optional, depending on your C implementation)
    # Here we would initialize centroids if needed. This step depends on your C code's expectations.

    # Perform k-means clustering
    libkmeans.kmeans(c_uint8(k), centroids, img.length * img.width * img.height, img.pixels)

    # Write the processed image to a new file
    if libkmeans.write_file(output_image_path, byref(img), centroids, c_uint8(k)) == -1:
        print("Failed to write the image")
        return

    print("Image processed and saved successfully.")

if __name__ == "__main__":
    example_usage()

