import time
import asyncio
from evdev import InputDevice, categorize, ecodes, InputEvent


async def main(dev: InputDevice):
    try:
        # Read a single event with timeout
        event = await asyncio.wait_for(dev.async_read_one(), timeout=0.1)
        if event:
            # Convert event to a categorized event
            categorized_event = categorize(event)

            # Get event type name
            event_type = ecodes.EV[event.type]

            # Get event code name (specific to the event type)
            if event.type == ecodes.EV_KEY:
                event_code = ecodes.KEY[event.code]
                event_value = (
                    "PRESSED"
                    if event.value == 1
                    else "RELEASED"
                    if event.value == 0
                    else "REPEAT"
                )
                print(f"Key Event: {event_code} {event_value}")
            elif event.type == ecodes.EV_ABS:
                event_code = ecodes.ABS[event.code]
                print(f"Absolute Event: {event_code} value={event.value}")
            elif event.type == ecodes.EV_REL:
                event_code = ecodes.REL[event.code]
                print(f"Relative Event: {event_code} value={event.value}")
            else:
                print(
                    f"Other Event: type={event_type} code={event.code} value={event.value}"
                )

    except asyncio.TimeoutError:
        pass
    except asyncio.exceptions.InvalidStateError:
        pass
    await asyncio.sleep(0.003)


async def run_loop(device):
    try:
        while True:
            await main(device)
            print("Long running Task")
            time.sleep(0.5)
            print("Loop continuing...")
    except KeyboardInterrupt:
        print("Stopping loop...")


if __name__ == "__main__":
    try:
        device = InputDevice("/dev/input/event9")
        asyncio.run(run_loop(device))
    except Exception as e:
        print(f"Error: {e}")
