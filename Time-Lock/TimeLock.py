# IMPORTS
from datetime import datetime
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

epochTime = datetime(int(es[0]), int(es[1]), int(es[2]), int(es[3]), int(es[4]), int(es[5]))
currentTime = datetime.now()

# debug
#epochTime = datetime(1974, 6, 1, 8, 57, 23)
currentTime = datetime(2017, 4, 26, 15, 14, 30)

# check if date is in DST
epochDST = False
currentDST = False
if (epochTime.month >= 3 and epochTime.month < 11):
    epochDST = True
if (currentTime.month >= 3 and currentTime.month < 11):
    currentDST = True

elapsedTime = (currentTime - epochTime).total_seconds()
elapsedTime = floor(elapsedTime - (elapsedTime % 60))
if ((epochDST and not currentDST) or (currentDST and not epochDST)):
    elapsedTime -= 3600
print(elapsedTime)

# compute MD5 hash
hashedTime = md5(str(elapsedTime).encode())
hashedTime = md5(hashedTime.hexdigest().encode())
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

