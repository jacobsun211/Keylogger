from pynput import keyboard

def on_press(key):
    # this function is tracking and printing all the keys the user is typing haha

    try:

        print(f'Key pressed: {key.char}')

    except AttributeError:

        print(f'Special key pressed: {key}')

listener = keyboard.Listener(on_press=on_press)

listener.start()
listener.join()