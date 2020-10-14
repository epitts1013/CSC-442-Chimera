import socket
from time import sleep
from random import randint

# set the port for client connections
port = 1337

# create the socket and bind it to the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))

# listen for clients
# this is a blocking call
s.listen(0)

# a client has connected!
c, addr = s.accept()

# set the message
msg = "Some message...\n"

covertMessage = "Testing..."
binaryMessage = ""
for char in covertMessage:
    binaryMessage += bin(ord(char))[2:].zfill(7)

print(binaryMessage)

# send the message, one letter at a time
for i in range(len(binaryMessage)):
	c.send(msg[i%len(msg)].encode())
	# delay a bit in between each letter
	if (binaryMessage[i] == "0"):
		sleep(0.025)
	else:
		sleep(0.1)

# send EOF and close the connection to the client
c.send("EOF".encode())
c.close()
