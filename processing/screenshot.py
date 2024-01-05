import subprocess

def take_screenshot(filename):
    """Takes a screenshot using KDE's spectacle tool"""
    # Using spectacle with flags -b (no GUI), -n (no notifications) and -o (output file)
    screenshot_command = ["spectacle", "-b", "-n", "-o", filename]
    process = subprocess.run(screenshot_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process.returncode == 0