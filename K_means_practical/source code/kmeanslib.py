'''
This script is a Python module that demonstrates how to use the kmeans 
C library in Python using ctypes.

How was the C library created?

The C library was created by compiling the kmeans.c file using the following command:
    gcc -shared -o libkmeans.so -fPIC kmeans.c
    
'''

from ctypes import *

# Define the ctypes equivalent of the C structs

class Cluster(Structure):
    """
    Represents a cluster in the K-means algorithm.

    Attributes:
        num_puntos (int): The number of points in the cluster.
        r (int): The red component of the cluster's color.
        g (int): The green component of the cluster's color.
        b (int): The blue component of the cluster's color.
        media_r (int): The average red component of the points in the cluster.
        media_g (int): The average green component of the points in the cluster.
        media_b (int): The average blue component of the points in the cluster.
    """
    _fields_ = [("num_puntos", c_uint32),
                ("r", c_uint8),
                ("g", c_uint8),
                ("b", c_uint8),
                ("media_r", c_uint32),
                ("media_g", c_uint32),
                ("media_b", c_uint32)]

class RGB(Structure):
    """
    Represents a color in the RGB color space.

    Attributes:
        b (int): The blue component of the color.
        g (int): The green component of the color.
        r (int): The red component of the color.
    """
    _fields_ = [("b", c_uint8),
                ("g", c_uint8),
                ("r", c_uint8)]

class Image(Structure):
    """
    Represents an image with its properties and pixel data.

    Attributes:
        length (int): The length of the image.
        width (int): The width of the image.
        height (int): The height of the image.
        header (bytes): The header data of the image.
        pixels (POINTER(RGB)): A pointer to the pixel data of the image.
        fp (c_void_p): A void pointer representing the FILE* of the image.
    """
    _fields_ = [("length", c_uint32),
                ("width", c_uint32),
                ("height", c_uint32),
                ("header", c_uint8 * 54),
                ("pixels", POINTER(RGB)),
                ("fp", c_void_p)]  # FILE* is treated as void pointer

# Define the Kmeans class
class Kmeans:

    # Constructor
    def __init__(self):
        # Import a shared library called "libkmeans.so" using the CDLL class from the ctypes module in Python.
        self.libkmeans = CDLL('/home/agarcias/Documents/UAB_year3/parallel_programming/parallel_programming_repo/K_means_practical/source code/libkmeans.so') 

    # Read file method
    def read_file(self, name, image):
        """
        Reads an image file and stores its properties and pixel data in the Image structure.

        Args:
            name (bytes): The name of the image file.
            image (Image): The Image structure to store the image data.

        Returns:
            int: 0 if the image was read successfully, -1 if there was an error.
        """
        return self.libkmeans.read_file(name, byref(image))

    # Write file method
    def write_file(self, output, image, clusters, k):
        """
        Writes the processed image to a new file.

        Args:
            output (bytes): The name of the output file.
            image (Image): The Image structure containing the processed image data.
            clusters (POINTER(Cluster)): A pointer to the array of Cluster structures representing the clusters.
            k (int): The number of clusters.

        Returns:
            int: 0 if the image was written successfully, -1 if there was an error.
        """
        return self.libkmeans.write_file(output, byref(image), clusters, k)

    # Get checksum method
    def getChecksum(self, clusters, k):
        """
        Computes the checksum of the clusters.

        Args:
            clusters (POINTER(Cluster)): A pointer to the array of Cluster structures representing the clusters.
            k (int): The number of clusters.

        Returns:
            int: The checksum of the clusters.
        """
        return self.libkmeans.getChecksum(clusters, k)
    
    # K-means computation method
    def kmeans_computation(self, k, img, clusters):
        """
        Perform k-means computation on an image.

        Args:
            k (int): The number of clusters.
            img (Image): The image object.
            clusters (int): The number of clusters.

        Returns:
            ndarray: The computed k-means result.
        """
        return self.libkmeans.kmeans(k, clusters, img.length, img.pixels)
    
    # K-means method
    def kmeans(self, k, name_file, output = None):
        """
        Perform k-means clustering on an image and write the processed image to a new file.

        Args:
            k (int): The number of clusters.
            name_file (bytes): The name of the original image file.
            output (bytes): The name of the output file.

        Returns:
            int: 0 if the image was processed and written successfully, -1 if there was an error.
        """
        # Instantiate the Image structure
        img = Image()

        # Convert the name_file to bytes
        # c_name_file = name_file.encode('utf-8')

        # Convert the output to bytes
        # c_output = output.encode('utf-8')

        # Instantiate the Cluster array
        c_clusters = (Cluster * k)()

        # Read the image file
        if self.read_file(name_file, img) == -1:
            print("\nFailed to read the image\n")
            return -1
        else:
            print("\nImage read successfully\n")

        # Perform k-means computation
        self.kmeans_computation(k, img, c_clusters)

        # Get the checksum of the clusters
        self.getChecksum(c_clusters, k)

        # Write the processed image to a new file
        if output is not None:
            if self.write_file(output, img, c_clusters, k) == -1:
                print("\nFailed to write the image\n")
                return -1

        print("\nImage processed and saved successfully.\n")
        print('-----------------------------------------')
        return 0

# [Unit test]
# Different unity test to check the functionality of the Kmeans class with different k.
def main():

    # Instantiate the Kmeans class
    kmeans = Kmeans()

    # Test with k = 3
    kmeans.kmeans(3, b'imagen.bmp', b'output_img3.bmp')

    # Test with k = 5
    kmeans.kmeans(5, b'imagen.bmp', b'output_img5.bmp')

    # Test with k = 10
    kmeans.kmeans(10, b'imagen.bmp', b'output_img10.bmp')

    # Test with k = 20
    kmeans.kmeans(20, b'imagen.bmp', b'output_img20.bmp')

    # Test with k = 50
    kmeans.kmeans(50, b'imagen.bmp', b'output_img50.bmp')

    # Test with k = 100
    kmeans.kmeans(100, b'imagen.bmp', b'output_img100.bmp')

if __name__ == "__main__":

    main()
