import time
import asyncio
from evdev import InputDevice, categorize, ecodes, list_devices


async def process_event(event, device_name):
    if event:
        categorized_event = categorize(event)
        event_type = ecodes.EV[event.type]

        if event.type == ecodes.EV_KEY:
            event_code = ecodes.KEY[event.code]
            event_value = (
                "PRESSED"
                if event.value == 1
                else "RELEASED"
                if event.value == 0
                else "REPEAT"
            )
            print(f"Device: {device_name} - Key Event: {event_code} {event_value}")
        elif event.type == ecodes.EV_ABS:
            event_code = ecodes.ABS[event.code]
            print(
                f"Device: {device_name} - Absolute Event: {event_code} value={event.value}"
            )
        elif event.type == ecodes.EV_REL:
            event_code = ecodes.REL[event.code]
            print(
                f"Device: {device_name} - Relative Event: {event_code} value={event.value}"
            )
        else:
            print(
                f"Device: {device_name} - Other Event: type={event_type} code={event.code} value={event.value}"
            )

def find_keyboards():
    devices = []
    for path in list_devices():
        try:
            device = InputDevice(path)
            # Filter for keyboard devices
            if any(word in device.name.lower() for word in ["keyboard", "kbd"]):
                devices.append(device)
                print(f"Found keyboard: {device.name} at {device.path}")
        except Exception as e:
            print(f"Error accessing device at {path}: {e}")
    return devices


async def run_multiple_keyboards():
    keyboards = find_keyboards()
    if not keyboards:
        print("No keyboards found!")
        return

    print(f"Monitoring {len(keyboards)} keyboards...")
    tasks = [monitor_device(device) for device in keyboards]
    await asyncio.gather(*tasks, return_exceptions=True)

async def monitor_device(device: InputDevice):
    try:
        event = await asyncio.wait_for(device.async_read_one(), timeout=0.05)
        if event:
            await process_event(event, device.name)
    except asyncio.TimeoutError:
        pass  # Expected timeout
    except (asyncio.exceptions.InvalidStateError, OSError) as e:
        print(f"Device {device.name} error: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    while True:  # Single main loop
        try:
            print("Starting keyboard monitoring system...")
            asyncio.run(run_multiple_keyboards())
            print("Restarting system in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nKeyboard monitoring system stopped by user")
            break
        except Exception as e:
            print(f"Fatal error occurred: {e}")
            print("Restarting system in 5 seconds...")
            time.sleep(5)