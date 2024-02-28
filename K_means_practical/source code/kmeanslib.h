#define MAX(a,b) ((a) > (b) ? a : b)
#define MIN(a,b) ((a) < (b) ? a : b)

/**
 * @brief Structure representing a cluster in the K-means algorithm.
 * 
 * This structure holds information about a cluster, including the number of points in the cluster,
 * the RGB color values of the cluster, and the average RGB values of the cluster.
 */
typedef struct {
	uint32_t num_puntos;    /**< Number of points in the cluster */
	uint8_t r, g, b;        /**< RGB color values of the cluster */
	uint32_t media_r, media_g, media_b;    /**< Average RGB values of the cluster */
} cluster;

/**
 * @brief Structure representing an RGB color.
 * 
 * This structure stores the red, green, and blue components of an RGB color.
 * Each component is represented by an 8-bit unsigned integer.
 */
typedef struct {
	uint8_t b, g, r;
} rgb;

/**
 * @brief Structure representing an image.
 * 
 * This structure holds information about an image, including its length, width, and height, as well as
 * the header of the image file, and the pixels of the image.
 */
typedef struct {
	uint32_t length;
	uint32_t width;
	uint32_t height;
	uint8_t header[54];
	
  rgb* pixels;
	
  FILE* fp;
} image;

int read_file(char *name, image* mImage);
int write_file(char *name, image *mImage, cluster *centroids, uint8_t k);
uint32_t getChecksum(cluster* centroids, uint8_t k);
uint8_t find_closest_centroid(rgb* p, cluster* centroids, uint8_t num_clusters);
void kmeans(uint8_t k, cluster* centroides, uint32_t num_pixels, rgb* pixels);
