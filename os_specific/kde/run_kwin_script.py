import os
import subprocess

script = os.path.abspath("./kwinActiveWindow.js")

# Load script
reg_script_number = subprocess.run("dbus-send --print-reply --dest=org.kde.KWin \
                    /Scripting org.kde.kwin.Scripting.loadScript \
                    string:" + script + " | awk 'END {print $2}'",
                        capture_output=True, shell=True).stdout.decode().split("\n")[0]

# Run script
subprocess.run("dbus-send --print-reply --dest=org.kde.KWin /" + reg_script_number + " org.kde.kwin.Script.run",
              shell=True, stdout=subprocess.DEVNULL)

# Stop script, not sure if needed
subprocess.run("dbus-send --print-reply --dest=org.kde.KWin /" + reg_script_number + " org.kde.kwin.Script.stop",
              shell=True, stdout=subprocess.DEVNULL)  # unregister number
