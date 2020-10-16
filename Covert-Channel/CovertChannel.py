from socket import socket, AF_INET, SOCK_STREAM
from sys import stdout
from time import time
from textwrap import wrap

DEBUG_MODE = True

# convert binary string to equivalent ascii text
def binaryConvert(content, length):
    text = ""

    wrapped_content = wrap(content, length)

    for character in wrapped_content:

        int_content = int(character, 2)
        text += chr(int_content)

    print("Solution : " + text)

# server information variables
serverIP = "138.47.98.190"
portNum = 31337

# set time threshold for "short" and "long" delay
delayThreshold = 0.1

# create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish connection to server
clientSocket.connect((serverIP, portNum))

# receive initial data packet from server
data = clientSocket.recv(4096)

# continue receiving data until recieving an EOF message
timeDeltas = []
while (data.decode().rstrip("\n") != "EOF"):
    # output data to stdout
    stdout.write(data.decode())
    stdout.flush()

    # get time until next message recieved
    startTime = time()
    data = clientSocket.recv(4096)
    endTime = time()
    timeDeltas.append(endTime - startTime)

if (DEBUG_MODE):
    orderedDeltas = timeDeltas.copy()
    orderedDeltas.sort()
    for delta in orderedDeltas:
        print(round(delta, 3))

binaryMessage = ""
for delta in timeDeltas:
    # calculate time between messages
    delta = round(delta, 3)

    # compare timeDelta to delayThreshold
    if (delta < delayThreshold):
        binaryMessage += "0"
    else:
        binaryMessage += "1"

print(binaryMessage)

binaryConvert(binaryMessage, 8)
