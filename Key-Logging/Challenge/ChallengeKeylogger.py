from pynput.keyboard import Listener, Key, Controller
from socket import socket, AF_INET, SOCK_STREAM
from sys import stdin, stdout
from random import uniform
from time import sleep, time

DEBUG = False

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

if (DEBUG):
    print(keysPressed)
    print(holdTimings)
    print(intervalTimings)

input("Press enter to continue")
for i in range(1, 6):
    print("Typing in {} seconds...".format(6-i))
    sleep(1)

# make keypresses
keyboard = Controller()

string = "".join(keysPressed)

for i in range(len(string)):
    keyboard.press(string[i])
    sleep(holdTimings[i])
    keyboard.release(string[i])
    sleep(intervalTimings[i])

print()
