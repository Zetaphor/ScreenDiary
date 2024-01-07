import os
import subprocess
from logger_config import get_logger

logger = get_logger()

script = os.path.abspath("os_specific/kde/kWinActiveWindow.js")

DEBUG_DBUS_WINDOW = bool(int(os.getenv('DEBUG_DBUS_WINDOW')))

def run_window_script():
    if DEBUG_DBUS_WINDOW:
        logger.debug("Running KWin script: " + script)
    # Load script
    reg_script_number = subprocess.run("dbus-send --print-reply --dest=org.kde.KWin \
                        /Scripting org.kde.kwin.Scripting.loadScript \
                        string:" + script + " | awk 'END {print $2}'",
                            capture_output=True, shell=True).stdout.decode().split("\n")[0]

    # Run script
    process = subprocess.run("dbus-send --print-reply --dest=org.kde.KWin /" + reg_script_number + " org.kde.kwin.Script.run",
                shell=True, stdout=subprocess.DEVNULL)

    if process.returncode != 0:
        logger.error("Failed to run KWin script: " + script)

    # Stop script, not sure if needed
    process = subprocess.run("dbus-send --print-reply --dest=org.kde.KWin /" + reg_script_number + " org.kde.kwin.Script.stop",
                shell=True, stdout=subprocess.DEVNULL)  # Unregister number

    return process.returncode == 0
