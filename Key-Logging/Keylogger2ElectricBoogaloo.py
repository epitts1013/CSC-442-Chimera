from pynput.keyboard import Controller
from time import sleep
from random import uniform
from sys import stdout

keyboard = Controller()

string = "This is a really long long loooooooong string"

for ch in string:
    keyboard.press(ch)
    sleep(uniform(0.02, 0.2))
    keyboard.release(ch)

print()