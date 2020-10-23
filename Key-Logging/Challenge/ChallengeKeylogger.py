from pynput.keyboard import Listener, Key, Controller
from socket import socket, AF_INET, SOCK_STREAM
from sys import stdin, stdout
from random import uniform
from time import sleep, time

keysPressed = []
holdTimings = []
intervalTimings = []

pressStartTime = 0
pressEndTime = 0
intervalStartTime = 0
intervalEndTime = 0


# read keypresses
def on_press(key):
    global pressStartTime
    intervalEndTime = time()
    intervalTimings.append(intervalEndTime - intervalStartTime)
    pressStartTime = time()
    try:
        keysPressed.append(key.char)
    except AttributeError:
        if (str(key) == "Key.space"):
            keysPressed.append(" ")
        elif (str(key) == "Key.esc"):
            pass

def on_release(key):
    global intervalStartTime
    pressEndTime = time()
    holdTimings.append(pressEndTime - pressStartTime)
    intervalStartTime = time()

    if (key == Key.esc):
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

intervalTimings = intervalTimings[1:]

print(keysPressed)
print(holdTimings)
print(intervalTimings)

# make keypresses
keyboard = Controller()

string = "".join(keysPressed)

for ch in string:
    keyboard.press(ch)
    sleep(uniform(0.02, 0.2))
    keyboard.release(ch)

print()
