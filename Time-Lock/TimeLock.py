# IMPORTS
import datetime
import re
from math import floor
from sys import stdin
from hashlib import md5

# VARIABLES
DEBUG = True
stdinEpoch = ""

# MAIN
# get epoch from stdin
stdinEpoch = stdin.read()
es = stdinEpoch.split(" ")

epochTime = datetime.datetime(int(es[0]), int(es[1]), int(es[2]), int(es[3]), int(es[4]), int(es[5]))
currentTime = datetime.datetime.now()

# debug
epochTime = datetime.datetime(1999, 12, 31, 23, 59, 59)
currentTime = datetime.datetime(2013, 5, 6, 7, 43, 25)

elapsedTime = (currentTime - epochTime).total_seconds()
elapsedTime = floor(elapsedTime - (elapsedTime % 60))
print(elapsedTime)

# compute MD5 hash
hashedTime = md5(str(elapsedTime).encode())
hashedTime = md5(hashedTime.hexdigest().encode())
print(hashedTime.hexdigest())

### EVERYTHING BELOW HERE WORKS ###

# get code from hashed time
code = ""
charPattern = re.compile("[A-Za-z]")
numPattern = re.compile("[0-9]")

# get first two characters from hashed time difference
counter = 0
for char in hashedTime.hexdigest():
    if (charPattern.match(char)):
        code += char
        counter += 1
        if (counter == 2):
            break

# get first two numbers from reversed hashed time difference
counter = 0
for char in hashedTime.hexdigest()[::-1]:
    if (numPattern.match(char)):
        code += char
        counter += 1
        if (counter == 2):
            break

# output code
print(code)

