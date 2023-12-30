from PIL import Image
import imagehash

def compare_images(image_path1, image_path2):
    """ Compare two images and return if they are identical using perceptual hash.

    Args:
        image_path1 (str): Path to the first image.
        image_path2 (str): Path to the second image.

    Returns:
        bool: True if images are identical, False otherwise.
    """
    # Open the images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Calculate the hash for each image
    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)

    # Compare the hash values
    return hash1 == hash2

# Example usage
image1_path = 'desktop.png'
image2_path = 'desktop.png'
are_identical = compare_images(image1_path, image2_path)
print("Images are identical:", are_identical)
