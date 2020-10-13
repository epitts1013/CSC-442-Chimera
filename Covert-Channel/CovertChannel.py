import socket, os
from sys import stdout
from time import time
import sys
from textwrap import wrap
import matplotlib.pyplot as pp


# Plots deltas into a 1-D scatter plots for visible differentiation
def d_plot(deltas):
	pp.plot(deltas, len(deltas)*[1], ".")
	pp.show()

# Decodes delta array into a bitstring
def decode(delta):
	mp = get_midpoint(deltas)
	decoded_text = ""
	for c in deltas:
		decoded_text += separate(mp,c)
	return decoded_text

# Returns a 1 or 0, determined by if the passed delta is above or below midpoint
def separate(midpoint,d):
	HIGH = 0.052
	LOW = 0.038
	#if(abs(d-LOW) < abs(d-HIGH)):
	#	return "0"
	#else:
	#	return "1"
	if(d < midpoint):
		return '1'
	else:
		return '0'

# Converts a bitstring to a utf string
def binary_convert(content, length = 7):
    text = ""

    #if (len(content) % length) == 0:
    content = content[:(len(content) - (len(content) % length))]

    wrapped_content = wrap(content, length)

    for character in wrapped_content:
        int_content = int(character, 2)
        text += chr(int_content)

    return (text)

# Calculates the midpoint for the set of deltas
def get_midpoint(deltas):
	total = 0.0
	for delta in deltas:
		total += delta
	return total/len(deltas)


# server information variables
ip = "138.47.98.190"
port = 31337

# create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# establish connection to server
clientSocket.connect((serverIP, portNum))

# receive initial data packet from server
data = clientSocket.recv(4096)

# Set of delta values, containing the delay for each character recieved
deltas = []

# receive data until EOF
data = s.recv(4096).decode('UTF-8')
while (data.rstrip("\n") != "EOF"):
	# output the data
	#stdout.write(data)
	#stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096).decode('UTF-8')
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	if (DEBUG):
		stdout.write(" {}\n".format(delta))
        # Subtracts ping to server from the current delta
		deltas.append(delta-os.system("ping -c 1 138.47.98.190"))
		stdout.flush()

# close the connection to the server
s.close()
# Plots the delta values from all recieved characters into a 1-D scatter plot
d_plot(deltas)
print("Midpoint: ",get_midpoint(deltas))
# Decodes the delta values into a bitstring, then into a utf string
print(binary_convert(decode(deltas)))

#deltas.sort()
#print(deltas)
