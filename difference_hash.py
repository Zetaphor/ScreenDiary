from PIL import Image
import imagehash

def compare_screenshots(image_path1, image_path2):
    """ Compare two screenshots using difference hash and determine if they are significantly different.

    Args:
        image_path1 (str): Path to the first screenshot.
        image_path2 (str): Path to the second screenshot.

    Returns:
        bool: True if screenshots are significantly different, False otherwise.
    """
    # Open the screenshots
    screenshot1 = Image.open(image_path1)
    screenshot2 = Image.open(image_path2)

    # Calculate the hash for each screenshot
    hash1 = imagehash.dhash(screenshot1)
    hash2 = imagehash.dhash(screenshot2)

    # Calculate the difference in hashes
    hash_difference = hash1 - hash2

    # Define a threshold for what you consider a 'significant' change
    threshold = 10  # This is an example value, you may need to adjust this

    # Check if the difference is above the threshold
    return hash_difference > threshold

# Example usage
screenshot1_path = 'desktop.png'
screenshot2_path = 'desktop.png'
significant_change = compare_screenshots(screenshot1_path, screenshot2_path)
print("Screenshots have significantly changed:", significant_change)
