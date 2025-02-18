# Exploration Keyboard Event

## Python Input Library

### evdev

#### Pros:

- Direct access to Linux input subsystem
- Low-level device control
- Native Linux support
- Can handle multiple input devices
- Supports raw input events

#### Cons:

- Linux-only
- Requires root privileges
- More complex API

Example usage:
```python
# evdev example
from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event0')
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
```
### keyboard (python-keyboard)

#### Pros:

- Cross-platform
- Simple API
- Hook-based event handling
- No root privileges needed (usually)

#### Cons:

- Less precise
- timing
- Limited device control
- No raw device access
  
Example usage:

```python
import keyboard

def on_key_event(e):
    print(f'Key {e.name} {"pressed" if e.event_type == "down" else "released"}')

keyboard.hook(on_key_event)
keyboard.wait()

```

### pynput

#### Pros

- Cross-platform (Windows, Linux, macOS)
- Clean object-oriented API
- Good documentation
- Supports both monitoring and control

#### Cons

- Higher-level abstraction
- May have platform-specific quirks
- No raw device access

Example usage:

```python
from pynput import keyboard

def on_press(key):
    print(f'Key {key} pressed')

def on_release(key):
    print(f'Key {key} released')

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
```

### pyxhook

#### Pros

- Lightweight X11 keyboard/mouse hooking
- No root privileges required
- Specific to Linux X11 systems
- Good for basic keyboard monitoring

#### Cons

- Limited maintenance and updates
- X11 specific (won't work with Wayland)
- Limited documentation
- No raw device access

Example usage:

```python
import pyxhook

def handle_keypress(event):
    print(f'Key {event.Key} pressed')

hook = pyxhook.HookManager()
hook.KeyDown = handle_keypress
hook.HookKeyboard()
hook.start()
```

### pyautogui

#### Pros

- Cross-platform support
- Rich GUI automation features
- Extensive documentation
- Simple API for keyboard/mouse control
- Active maintenance

#### Cons

- Higher-level abstraction
- No raw input device access
- Can be slower for pure keyboard monitoring
- Limited multi-keyboard support
- Screen-coordinate dependent

Example usage:

```python
import pyautogui

# Basic keyboard monitoring
pyautogui.FAILSAFE = True
pyautogui.write('Hello')
pyautogui.keyDown('ctrl')
pyautogui.press('c')
pyautogui.keyUp('ctrl')
```

### Xlib

#### Pros

- Low-level X Window System access
- Highly customizable
- Direct X11 protocol interaction
- Can handle multiple input devices
- Good for complex X11 applications

#### Cons

- Steep learning curve
- Complex API
- X11 specific
- Requires good understanding of X protocol
- Limited modern documentation

Example usage:

```python
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

def callback(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        return
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(
            data, display.Display().display, None, None)
        if event.type == X.KeyPress:
            print(f"Key pressed: {event.detail}")

d = display.Display()
ctx = d.record_create_context(
    0,
    [record.AllClients],
    [{
        'core_requests': (0, 0),
        'core_replies': (0, 0),
        'ext_requests': (0, 0, 0, 0),
        'ext_replies': (0, 0, 0, 0),
        'delivered_events': (0, 0),
        'device_events': (X.KeyPress, X.KeyRelease),
        'errors': (0, 0),
        'client_started': False,
        'client_died': False,
    }])
```

### pythoncom (Windows-specific)

#### Pros

- Deep Windows API integration
- Reliable Windows event handling
- Part of well-maintained pywin32
- Good for Windows-specific applications

#### Cons

- Windows-only
- Complex setup
- Requires pywin32
- Steep learning curve
- Not suitable for cross-platform

Example usage:

```python
import pythoncom
import pyHook

def OnKeyboardEvent(event):
    print(f'KeyID: {event.KeyID}')
    print(f'Key: {event.Key}')
    return True

hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
```

## Installation Commands

```bash
# Install pyxhook
pip install pyxhook

# Install pyautogui
pip install pyautogui

# Install python-xlib
pip install python-xlib

# Install pywin32 (Windows only)
pip install pywin32
```

## Python Input Device Libraries Comparison

### MultiKeyboard Libraries with Focus on Ease of Use

#### `evdev` - Linux Input Device Library

```python
from evdev import InputDevice, categorize, ecodes

# Example showing multi-keyboard handling
def list_devices():
    devices = [InputDevice(fn) for fn in list_devices()]
    for device in devices:
        if "keyboard" in device.name.lower():
            print(f"Found keyboard: {device.name}")
            monitor_keyboard(device)

def monitor_keyboard(device):
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            print(f"Device {device.name}: {categorize(event)}")
```

#### `pynput` - Cross-platform Solution

```python
from pynput import keyboard
import threading

# Example of handling multiple keyboards
def start_listener(device_id):
    def on_press(key):
        print(f'Keyboard {device_id}: {key} pressed')

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start multiple listeners
for i in range(2):  # For 2 keyboards
    thread = threading.Thread(target=start_listener, args=(i,))
    thread.start()
```

#### Comparison Matrix

| Feature        | evdev | pynput | keyboard | pyxhook | pyautogui |
| -------------- | ----- | ------ | -------- | ------- | --------- |
| Multi-keyboard | ✅    | ⚠️     | ❌       | ❌      | ❌        |
| Easy Setup     | ⚠️    | ✅     | ✅       | ⚠️      | ✅        |
| Root Required  | ✅    | ❌     | ❌       | ❌      | ❌        |
| Raw Events     | ✅    | ❌     | ❌       | ✅      | ❌        |
| Linux Support  | ✅    | ✅     | ✅       | ✅      | ✅        |
| Cross-platform | ❌    | ✅     | ✅       | ❌      | ✅        |

#### Installation Commands

```bash
# For evdev
sudo pip install evdev

# For pynput
pip install pynput

# For keyboard
pip install keyboard

# For pyxhook
pip install pyxhook

# For pyautogui
pip install pyautogui
```

#### Recommendation

- For **multiple keyboard handling** on Linux: Use `evdev`
- For **cross-platform** needs: Use `pynput`
- For **simple single keyboard** tasks: Use `keyboard` or `pyautogui`
- For **X11-specific** needs: Use `pyxhook`

**Note**: For handling multiple keyboards, `evdev` is the most reliable option on Linux, though it requires root privileges. `pynput` can handle multiple keyboards in some cases but may have limitations depending on the system configuration.
