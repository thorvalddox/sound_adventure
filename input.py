from evdev import InputDevice, list_devices, ecodes


def search_keypad():
    found = False
    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
        print("found:", dev.name)
        if "Keypad" in dev.name:
            return dev

    if not found:
        print('Keypad not found. Aborting ...')
        raise SystemExit

class InputReader():
    def __init__(self):
        self.device = search_keypad()
    def __call__(self):
        for event in self.device.read_loop():
            if event.type == 1 and event.value == 1 and event.code != 69:
                yield {82:"0",79:"1",80:"2",81:"3",75:"4",76:"5",77:"6",71:"7",72:"8",73:"9",
                       98:"/",55:"*",78:"+",74:"-",14:"<",83:".",96:"\n"}[event.code]
