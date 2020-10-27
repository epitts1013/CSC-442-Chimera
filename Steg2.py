#My code doesn't work for the most part.  It works when I use example files, but when I use the given files on the site, it retrieves the wrong text. I got stuck on the byte method so I wasn't able to work on the bit retrieve method

from sys import stdin, argv
import sys
import os
import binascii
import argparse

Sentinel = ['00000000', '11111111', '00000000', '00000000', '11111111', '00000000']

######## Arguments
parser = argparse.ArgumentParser(add_help= False)
parser.add_argument("-r", action = "store_true")
parser.add_argument("-s", action = "store_true")
parser.add_argument("-b", action = "store_true")
parser.add_argument("-B", action = "store_true",)
parser.add_argument("-o", default = 0, type=int)
parser.add_argument("-i", default = 1, type=int)
parser.add_argument("-w", type=str)
parser.add_argument("-h", type=str)
args = parser.parse_args()

#Stores the hidden file into the wrapper file
if args.s:
	wrapper = map(bin,bytearray((open(args.w, "r++").read()).replace('\n', '')))
	hidden = map(bin,bytearray((open(args.h, "r++").read()).replace('\n', '')))
	offset = args.o
	interval = args.i
	i = 0
	while i < len(wrapper):
		wrapper[i] = wrapper[i].replace('0b' , '').zfill(8)
		i +=1
	i = 0
	while i < len(hidden):
		hidden[i] = hidden[i].replace('0b' , '').zfill(8)
		i +=1
    #Uses the Byte method to store the hidden file
	if args.B:
		i = 0
		while i < len(hidden):
			wrapper[offset] = hidden[i]
			i += 1
			offset += interval	
		i = 0
		while i < len(Sentinel):
			wrapper[offset] = Sentinel[i]
			offset += interval
			i +=1
		i = 0
		text = ""
		while i < len(wrapper):
			text += chr(int(wrapper[i],2))
			i +=1
		sys.stdout.write(text)
        
    #Uses the bit method to store the hidden file
	if args.b:
		i = 0
		while i < len(hidden):
			for j in range(8):
				print wrapper[offset]
				j = bin(wrapper[offset] & '11111110').replace('0b', '').zfill(8)
				print j
				wrapper[offset] |= ((hidden[i] & 10000000) >> 7)
				hidden[i] = (hidden[i] << 1) & (2 ** 8 -1)
				offset += interval
			i +=1
		i = 0
		while i < len(Sentinel):
			for j in range(8):
				wrapper[offset] &= 11111110
				wrapper[offset] |= ((Sentinel[i] & 10000000) >> 7)
				Sentinel[i] = (Sentinel[i] << 1) & (2 ** 8 -1)
				offset += interval
			i +=1
		i = 0
		text = ""
		while i < len(wrapper):
			text += chr(int(wrapper[i],2))
			i +=1
		sys.stdout.write(text)
		        

#Retrieves the hidden file from the wrapper file
if args.r:
	wrapper = map(bin,bytearray((open(args.w, "r++").read()).replace('\n', '')))
	#Uses the Byte method to retrieve the hidden file
	if args.B:
		i = 0
		while i < len(wrapper):
			wrapper[i] = wrapper[i].replace('0b' , '').zfill(8)
			i +=1
		offset = args.o
		interval = args.i
		hidden = []
		i = 0
		while offset < len(wrapper) and hidden[-6:] != Sentinel:
			hidden.append(wrapper[offset])
			offset += interval
		hidden = hidden[:(len(hidden)-6)]
		i = 0
		text = ""
		while i < len(hidden):
			text += chr(int(hidden[i],2))
			i +=1
		sys.stdout.write(text)
	if args.b:
		pass
		
		
