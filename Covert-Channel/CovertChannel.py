from socket import socket, AF_INET, SOCK_STREAM
from sys import stdout
from time import time

# server information variables
serverIP = "localhost"  # change this to actual server IP when trying on Timo's server
portNum = 1337

# set time threshold for "short" and "long" delay
delayThreshold = 0.5

# create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish connection to server
clientSocket.connect((serverIP, portNum))

# receive initial data packet from server
data = clientSocket.recv(4096)

# continue receiving data until recieving an EOF message
binaryMessage = ""
while (data.decode().rstrip("\n") != "EOF"):
    # output data to stdout
    stdout.write(data.decode())
    stdout.flush()

    # get time until next message recieved
    startTime = time()
    data = clientSocket.recv(4096)
    endTime = time()

    # calculate time between messages
    timeDelta = round(endTime - startTime, 3)

    # compare timeDelta to delayThreshold
    if (timeDelta < delayThreshold):
        binaryMessage += 0
    else:
        binaryMessage += 1
