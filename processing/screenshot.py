import subprocess

def take_screenshot(filename):
    """
    Takes a screenshot using KDE's spectacle tool
    Replace this with your own WM specific screenshot command
    """
    # Using spectacle with flags -a (active window), -b (no GUI), -n (no notifications) and -o (output file)
    screenshot_command = ["spectacle", "-a", "-b", "-n", "-o", filename]
    process = subprocess.run(screenshot_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process.returncode == 0