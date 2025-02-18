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
                # Use a shorter timeout to be more responsive
                event = await asyncio.wait_for(device.async_read_one(), timeout=0.05)
                if event:
                    await process_event(event, device.name)
            except asyncio.TimeoutError:
                # Expected timeout, continue monitoring
                continue
            except (asyncio.exceptions.InvalidStateError, OSError) as e:
                # Device might be disconnected or in invalid state
                print(f"Device {device.name} error: {e}")
                break  # Exit the monitoring loop for this device
            except Exception as e:
                print(f"Unexpected error monitoring {device.name}: {e}")
                break
            
            # Small sleep to prevent CPU overload
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Fatal error monitoring device {device.name}: {e}")
    finally:
        try:
            device.close()
        except:
            pass  # Ignore errors during cleanup


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
    while True:  # Main monitoring loop
        try:
            keyboards = find_keyboards()
            if not keyboards:
                print("No keyboards found! Retrying in 5 seconds...")
                await asyncio.sleep(5)
                continue

            print(f"Monitoring {len(keyboards)} keyboards...")
            tasks = [monitor_device(device) for device in keyboards]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # If we get here, all tasks have completed (probably due to errors)
            print("All keyboard monitoring tasks ended. Restarting...")
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            print("Stopping keyboard monitoring...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_multiple_keyboards())
    except Exception as e:
        print(f"Error: {e}")