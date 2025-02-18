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
            print(f"Device: {device_name} - Absolute Event: {event_code} value={event.value}")
        elif event.type == ecodes.EV_REL:
            event_code = ecodes.REL[event.code]
            print(f"Device: {device_name} - Relative Event: {event_code} value={event.value}")
        else:
            print(
                f"Device: {device_name} - Other Event: type={event_type} code={event.code} value={event.value}"
            )

async def monitor_device(device: InputDevice):
    try:
        while True:
            try:
                event = await asyncio.wait_for(device.async_read_one(), timeout=0.1)
                await process_event(event, device.name)
            except asyncio.TimeoutError:
                pass
            except asyncio.exceptions.InvalidStateError:
                pass
            await asyncio.sleep(0.003)
    except Exception as e:
        print(f"Error monitoring device {device.name}: {e}")

def find_keyboards():
    devices = []
    for path in list_devices():
        try:
            device = InputDevice(path)
            # Filter for keyboard devices
            if any(word in device.name.lower() for word in ['keyboard', 'kbd']):
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

    try:
        # Create tasks for each keyboard
        tasks = [monitor_device(device) for device in keyboards]
        print(f"Monitoring {len(keyboards)} keyboards...")
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("Stopping keyboard monitoring...")
    finally:
        for device in keyboards:
            device.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_multiple_keyboards())
    except Exception as e:
        print(f"Error: {e}")