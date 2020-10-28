# IMPORTS
import time
import re
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

# debug mode allows manual time entry
if (DEBUG):
    stdinEpoch = "2017 01 01 00 00 00"
    currentTime = time.mktime(time.strptime("2017 03 23 18 02 06", "%Y %m %d %H %M %S"))
    currentTime = currentTime - (currentTime % 60)

# get time of inputted epoch
epochTime = time.mktime(time.strptime(stdinEpoch, "%Y %m %d %H %M %S"))

# get time elapsed since given epoch
elapsedTime = currentTime - epochTime

# compute MD5 hash
hashedTime = md5(str(elapsedTime).encode())
print(hashedTime.hexdigest())

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

