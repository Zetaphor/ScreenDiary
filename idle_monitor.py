from evdev import InputDevice, ecodes
import select
import evdev
import threading

class IdleMonitor:
    def __init__(self):
        self.inactivity_detected = False
        self.inactivity_timer = None
        self.devices = [InputDevice(path) for path in evdev.list_devices()]
        self.fd_to_device = {dev.fd: dev for dev in self.devices}
        self.timer_lock = threading.Lock()

    def on_inactivity(self):
        with self.timer_lock:
            self.inactivity_detected = True

    def reset_timer(self):
        with self.timer_lock:
            if self.inactivity_timer:
                self.inactivity_timer.cancel()
            self.inactivity_detected = False
            self.inactivity_timer = threading.Timer(10.0, self.on_inactivity)
            self.inactivity_timer.start()

    def monitor_input(self):
        while True:
            self.reset_timer()
            r, w, x = select.select(self.fd_to_device, [], [])
            for fd in r:
                for event in self.fd_to_device[fd].read():
                    self.reset_timer()
                    # if event.type == ecodes.EV_KEY:
                    #     print(f'Key interaction: {event}')
                    # elif event.type in [ecodes.EV_REL, ecodes.EV_ABS]:
                    #     print(f'Mouse movement: {event}')

    def has_inactivity(self):
        return self.inactivity_detected
