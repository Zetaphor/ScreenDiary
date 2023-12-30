import subprocess
import time

def take_screenshot(filename):
    """
    Takes a screenshot using KDE's 'spectacle' command without GUI and notifications,
    then saves it with the given filename.
    """
    # Using spectacle with flags -b (no GUI), -n (no notifications) and -o (output file)
    subprocess.run(["spectacle", "-a", "-b", "-n", "-o", filename])

def main():
    counter = 1
    try:
        while True:
            screenshot_file = f"screenshots/screenshot_active_{counter}.png"
            take_screenshot(screenshot_file)
            print(f"Screenshot taken: {screenshot_file}")
            counter += 1
            time.sleep(2)  # Wait for 2 seconds before taking the next screenshot
    except KeyboardInterrupt:
        print("Screenshot taking stopped.")

if __name__ == "__main__":
    main()
