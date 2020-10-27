### Libraries
import argparse
import getopt
import sys

### Globals
SENTINEL = bytearray([0,255,0,0,255,0]) # sequence of bytes to signal hidden EOF

def usage():
    usage = '''Steg.py
            python3 Steg.py -(sr) -(bB) -o <val> [-i <val>] -w <val> [-h <val>] [-d]
            -s       store
            -r       retrieve
            -b       bit mode
            -B       byte mode
            -o <val> set offset to <val> (default is 0)
            -i <val> set interval to <val> (default is 1)
            -w <val> set wrapper file to <val>
            -h <val> set hidden file to <val
            --help   prints this message, that's it...
            -d       turn DEBUG mode on\n
            Progam requires that -s or -r, -b or -B, and -w <val> are specified.
            Output is to stdout and can be redirected using > 'filename'
            '''
    return usage


def get_wrapper(filename):
    try:
        with open(filename, mode='rb') as fp:
        # restrict the max size of input files by specifying read(size) just in case
            wrapper = bytearray(fp.read())
    except:
        print("Error opening {} wrapper file.".format(filename))
        return
    return wrapper

def get_hidden(filename):
        try:
            with open(filename, "rb") as fp:
            # restrict the max size of input files by specifying read(size)
                hidden = bytearray(fp.read())
        except:
            print("Error opening {} wrapper file.".format(filename))
            return
        return hidden

def output(output):
    try:
        if args.d:
            with open(StegOutput,"wb") as ofp:
                ofp.write(output)
                print("You're in debug mode so output is redirected to file *StegOutput*")
                print("Because we don't want debug print statments in the output file.")
                print("If your redirected stdout, hopefully you find this helpful and not annoying")
        else:
            sys.stdout.buffer.write(output)
    except:
        print("Something bad happend when creating the output. Try debug mode(-d)?")

parser = argparse.ArgumentParser(usage = usage(), add_help= False, description="Program to retieve or store hidden information with a file")
function = parser.add_mutually_exclusive_group(required=True)
mode = parser.add_mutually_exclusive_group(required=True)
function.add_argument("-s", help= "store", action="store_true")
function.add_argument("-r", help= "retrieve", action="store_true")
mode.add_argument("-b", help= "bit mode", action="store_true")
mode.add_argument("-B", help="byte mode", action="store_true")
parser.add_argument("-o", help="set offset to <val> (default is 0)", default= 0, type=int)
parser.add_argument("-i", help="set interval to <val> (default is 1)", default= 1, type=int)
parser.add_argument("-w", type=str)
parser.add_argument("-h", type=str)
parser.add_argument("--help", action="store_true")
parser.add_argument("-d", help= "turn DEBUG mode on", action="store_true")
args =parser.parse_args()

if args.help:
    print("This is your help message. If you made it here goo luck.")
    print(usage())
    sys.exit()
if args.d:
    DEBUG = True
    print("debug mode is on.")
if args.s:
    # storage mode, for storing a file in a get_wrapper
    # first determine if this is the bit or byte method

    if args.b: ### BIT METHOD
        if args.d:
            print("Storage mode using bit method")
            print("Wrapper filename is {}".format(args.w))
            print("Hidden filename is {}".format(args.h))
        # get the wrapper and hidden files + their lengths
        wrapper = get_wrapper(args.w) # wrapper is a byte array of the wrapper file
        wrapper_len = len(wrapper)
        hidden = get_hidden(args.h)
        hidden_len = len(hidden)
        if (hidden_len > wrapper_len):
            sys.exit("Error: Hidden file exceeds Wrapper in size, try again.")

        ctr = 0
        offset = args.o
        interval = args.i
        while (ctr < hidden_len):
            for j in [0,1,2,3,4,5,6,7]:
                wrapper[offset] = wrapper[offset] & 0b11111110 #zero out the LSB
                # take the MSB of hidden byte shift to right 7 places
                wrapper[offset] = wrapper[offset] | ((hidden[ctr] & 0b10000000) >> 7)
                # shift the hidden byte to the left one
                hidden[ctr] = (hidden[ctr] << 1) & (2 ** 8 - 1)
                offset += interval
            ctr += 1
            # end of input of hidden message, next insert SENTINEL
        # Note: offset is adjusted at the end of the for loop, so the ptr doesn't
              # need to be adjusted here.
        ctr = 0 #reset ctr to 0
        while (ctr < len(SENTINEL)):
            for j in [0,1,2,3,4,5,6,7]:
                wrapper[offset] = wrapper[offset] & 0b11111110 #zero out the LSB
                # take the MSB of hidden byte shift to right 7 places
                wrapper[offset] = wrapper[offset] | ((SENTINEL[ctr] & 0b10000000) >> 7)
                # shift the hidden byte to the left one
                SENTINEL[ctr] = (SENTINEL[ctr] << 1) & (2 ** 8 - 1)
                offset += interval
            ctr += 1
            # end of SENTINEL input
        # end of while loop
        # at this point wrapper contains hidden and we just need to output it
        output(wrapper)
        sys.exit() # close the program to same time

    if args.B: ### BYTE METHOD
        if args.d:
            print("Storage mode using byte method")
            print("Wrapper filename is {}".format(args.w))
            print("Hidden filename is {}".format(args.h))
        # get the wrapper and hidden files + their lengths
        wrapper = get_wrapper(args.w) # wrapper is a byte array of the wrapper file
        wrapper_len = len(wrapper)
        hidden = get_hidden(args.h)
        hidden_len = len(hidden)

        ctr = 0
        offset = args.o
        interval = args.i
        # Basically replace the an entire byte of the wrapper with a byte of the
        # hidden file and then add the sentinel bytes.
        while (ctr < hidden_len):
            wrapper[offset] = hidden[ctr]
            offset += interval
            ctr += 1
        # end while
        ctr = 0
        while (ctr < len(SENTINEL)):
            wrapper[offset] = SENTINEL[ctr]
            offset += interval
            ctr += 1
        # end of while loop
        output(wrapper)
        sys.exit() # close the program to same time

if args.r:
    # retrieve mode for retrieving a hidden file from a wrapper aka extraction
    # first determin if this is the bit or byte method
    if args.b: ### BIT METHOD
        if args.d:
            print("Storage mode using bit method")
            print("Wrapper filename is {}".format(args.w))
            print("Hidden filename is {}".format(args.h))
        wrapper = get_wrapper(args.w) # wrapper is a byte array of the wrapper file
        wrapper_len = len(wrapper)
        hidden = bytearray() # location of hidden message

        offset = args.o
        interval = args.i
        pos_eof = bytearray() # possible eof byte array equal to SENTINEL
        while (offset < wrapper_len):
            b = 0b00000000 # set b = to a 0 byte
            for j in [0,1,2,3,4,5,6,7]: # create b from the hidden bits
                b = b | (wrapper[offset] & 0b00000001)
                if (j < 7):
                    b = (b << 1) & (2 ** 8 - 1)
                    offset += interval
            if (b == SENTINEL[0]): # check to see if b matches 1st byte in SENTINEL
                pos_eof.append(b) # add b to the possible EOF bytearray
                # increment the offset and check the next byte
                offset += interval
                b = 0b00000000
                for j in [0,1,2,3,4,5,6,7]:
                    b = b | (wrapper[offset] & 0b00000001)
                    if (j < 7):
                        b = (b << 1) & (2 ** 8 - 1)
                        offset += interval

                if (b == SENTINEL[1]): #if the second byte matches, might as well check the next 4
                    pos_eof.append(b) # add b to the possible EOF bytearray
                    offset += interval # increment the offset
                    gg = 2 #counter variable
                    while (gg < len(SENTINEL)): #len of SENTINEL = 6 so this loops 4 times
                        b = 0b00000000
                        for j in [0,1,2,3,4,5,6,7]:
                            b = b | (wrapper[offset] & 0b00000001)
                            if (j < 7):
                                b = (b << 1) & (2 ** 8 - 1)
                                offset += interval
                        # after getting the new b, add it to pos_eof, increment gg and offset
                        pos_eof.append(b)
                        offset += interval
                        gg += 1
                    # now pos_eof is a 6 byte array and if it matches SENTINEL we done
                    if (pos_eof == SENTINEL):
                        #done
                        output(hidden)
                        sys.exit()

                    # if it don't match, add pos_eof to the hidden message
                    # set pos_eof back to an empty bytearray and keep going
                    else:
                        hidden.extend(pos_eof) # adds pos_eof to the end of hidden
                        pos_eof = bytearray() # reset pos_eof to an empty bytearray
                    # Note we have already added b to hidden and incremented offset.

                else: # SENTINEL[1] doesn't match b, so add the two bytes parsed and keep going
                    hidden.extend(pos_eof) # adds pos_eof to the end of hidden
                    pos_eof = bytearray() # reset pos_eof to an empty bytearray
                    hidden.append(b) # add the b value to hidden
                    offset += interval

            else: # b doesn't match 1st SENTINEL byte so keep going
                hidden.append(b)
                offset += interval
        # End of major while loop

    if args.B: ### BYTE method
        if args.d:
            print("Storage mode using bit method")
            print("Wrapper filename is {}".format(args.w))
            print("Hidden filename is {}".format(args.h))
        wrapper = get_wrapper(args.w) # wrapper is a byte array of the wrapper file
        wrapper_len = len(wrapper)
        hidden = bytearray() # location of hidden message

        offset = args.o
        interval = args.i
        pos_eof = bytearray() # array to check for end of hidden file
        while (offset < wrapper_len):
            b = wrapper[offset]
            # check if b is the same as 1st SENTINEL byte
            if (b == SENTINEL[0]):
                pos_eof.append(b)
                offset += interval
                # check the 2nd byte
                b = wrapper[offset]
                if (b == SENTINEL[1]):
                    pos_eof.append(b)
                    offset += interval
                    # check the 3rd byte
                    b = wrapper[offset]
                    if (b == SENTINEL[2]):
                        pos_eof.append(b)
                        offset += interval
                        # check the 4th byte
                        b = wrapper[offset]
                        if (b == SENTINEL[3]):
                            pos_eof.append(b)
                            offset += interval
                            # check the 5th byte
                            b = wrapper[offset]
                            if (b == SENTINEL[4]):
                                pos_eof.append(b)
                                offset += interval
                                # check the 6th byte and final byte
                                b = wrapper[offset]
                                if (b == SENTINEL[5]): # same as pos_eof == SENTINEL
                                    pos_eof.append(b)
                                    output(hidden)
                                    
                                    sys.exit()
                                else:
                                    hidden.extend(pos_eof)
                                    pos_eof = bytearray()
                                    hidden.append(b)
                                    offset += interval
                        else:
                            hidden.extend(pos_eof)
                            pos_eof = bytearray()
                            hidden.append(b)
                            offset += interval
                    else:
                        hidden.extend(pos_eof)
                        pos_eof = bytearray()
                        hidden.append(b)
                        offset += interval
                else:
                    hidden.extend(pos_eof)
                    pos_eof = bytearray()
                    hidden.append(b)
                    offset += interval
            else:
                hidden.append(b)
                offset += interval
        # end of major while loop

if (args == []):
    usage()
    sys.exit(2)
