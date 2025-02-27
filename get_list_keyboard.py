from evdev import InputDevice, categorize, ecodes, list_devices

for path in list_devices():
        try:
            device = InputDevice(path)
            # Filter for keyboard devices
            if any(word in device.name.lower() for word in ["keyboard", "kbd"]):
                print(f"Found keyboard: {device.name} at {device.path}")
        except Exception as e:
            print(f"Error accessing device at {path}: {e}")