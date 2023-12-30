import subprocess

def take_screenshot(filename):
    """Takes a screenshot using KDE's spectacle tool"""
    # Using spectacle with flags -b (no GUI), -n (no notifications) and -o (output file)
    subprocess.run(["spectacle", "-a", "-b", "-n", "-o", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
