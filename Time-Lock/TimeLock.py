# IMPORTS
import time
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

# get current time rounded to last minute
currentTime = time.time() - (time.time() % 60)

# get time of inputted epoch
epochTime = time.mktime(time.strptime(stdinEpoch, "%Y %m %d %H %M %S"))

# debug mode allows manual time entry
if (DEBUG):
    stdinEpoch = "1999 12 31 23 59 59"
    currentTime = "2017 04 23 18 02 30"
    currentTime = time.mktime(time.strptime(currentTime, "%Y %m %d %H %M %S"))
    print(currentTime)
    currentTime = currentTime - (currentTime % 60)
    print(currentTime)
    epochTime = time.mktime(time.strptime(stdinEpoch, "%Y %m %d %H %M %S"))
    print(epochTime)

# get time elapsed since given epoch
elapsedTime = currentTime - epochTime

print(floor(elapsedTime))

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

