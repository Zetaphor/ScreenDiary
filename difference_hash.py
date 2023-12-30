from PIL import Image
import imagehash

def difference_hash(image_path1, image_path2):
  """ Compare two images and return if they are identical using difference hash.

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
  hash1 = imagehash.dhash(image1)
  hash2 = imagehash.dhash(image2)

  # Compare the hash values
  return hash1 == hash2