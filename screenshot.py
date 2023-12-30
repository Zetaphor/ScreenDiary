import subprocess
import time

def take_screenshot(filename):
    """
    Takes a screenshot using KDE's 'spectacle' command without GUI and notifications,
    then saves it with the given filename.
    """
    # Using spectacle with flags -b (no GUI), -n (no notifications) and -o (output file)
    subprocess.run(["spectacle", "-a", "-b", "-n", "-o", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
