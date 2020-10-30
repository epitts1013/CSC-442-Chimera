import sys
import math
from pathlib import Path

# Parses the command line arguments into variables.
def parse_args():
    args = sys.argv[1:]
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file
    global argvs
    for arg in args:
        arg_h = arg[0:2]
        if (arg_h == '-s'):
            store_mode = True
        elif (arg_h == '-r'):
            store_mode = False
        elif (arg_h == '-b'):
            bit_mode = True
        elif (arg_h == '-B'):
            bit_mode = False
        elif (arg_h == '-o'):
            offset = int(arg[2:])
        elif (arg_h == '-i'):
            interval = int(arg[2:])
        elif (arg_h == '-w'):
            if(Path(arg[2:]).is_file()):
                wrapper_file = bytearray(open(arg[2:], 'rb').read())
                argvs["wrapper"] = arg[2:]
            else:
                raise Exception("No file (wrapper file) with name : ", arg[2:])
                exit(0)
        elif (arg_h == '-h'):
            if(Path(arg[2:]).is_file()):
                hidden_file = bytearray(open(arg[2:], 'rb').read())
            else:
                raise Exception("No file (hidden file) with name : ", arg[2:])
                exit(0)


# Calculates the largest interval possible for
# byte-based storage
def byte_optimal_interval(SENTINEL,wrapper_file,offset,hidden_file):
    return (math.floor((len(wrapper_file) - offset) / (len(hidden_file) + len(SENTINEL))))


# Stores the input hidden file into the input wrapper
# file using the byte method.
def byte_store(SENTINEL,offset,interval,wrapper_file,hidden_file):
    if(interval > byte_optimal_interval(SENTINEL,wrapper_file,offset,hidden_file)):  # Checks if supplied interval is too large for wrapper file
        raise Exception("Interval value too large.")

    for i in range(len(hidden_file)):  # Hides the hidden file into the wrapper file
        wrapper_file[offset] = hidden_file[i]
        offset += interval

    for i in range(len(SENTINEL)):  # Appends the SENTINEL
        wrapper_file[offset] = SENTINEL[i]
        offset += interval

    out = open(argvs["wrapper"], 'rb+')  # Opens the wrapper file to write to write changes
    out.write(wrapper_file)  # Writes the edited wrapper file
    out.close()


# Extracts the file hidden in the hidden file using the byte method.
# The extracted file is output to stdout as binary data.
def byte_extract(SENTINEL,offset,interval,wrapper_file):
    s_matches = 0  # SENTINEL matches / position in SENTINEL
    s_len = len(SENTINEL)  # Length of the SENTINEL
    out = []  # Output file data as an array of bytes

    for i in range(offset, len(wrapper_file), interval):
        byte = wrapper_file[i]
        out.append(byte)

        if (byte == SENTINEL[s_matches]):  # Checks if byte equals current position of SENTINEL
            s_matches += 1  # Byte matches current position of SENTINEL
            if (s_matches == s_len):  # All bytes of SENTINEL matched
                out = out[:-len(SENTINEL)]  # Remove the SENTINEL from output file
                return bytearray(out)
        else:
            s_matches = 0

    raise Exception("SENTINEL not found.")  # SENTINEL not found in the input file


# Extracts the file hidden in the hidden file using the bit method.
# The extracted file is output to stdout as binary data.
def bit_extract(SENTINEL,offset,interval,wrapper_file):
    s_matches = 0  # SENTINEL matches / position in SENTINEL
    s_len = len(SENTINEL)  # Length of the SENTINEL
    out = []  # Output file data as an array of bytes
    while offset < (len(wrapper_file) - (interval * 8)):

        byte = 0
        for j in range(8):
            byte |= (wrapper_file[offset] & 1)
            if (j < 7):
                byte = (byte << 1 & 254)
            offset += interval
        out.append(byte)

        if (byte == SENTINEL[s_matches]):  # Checks if byte equals current position of SENTINEL
            s_matches += 1  # Byte matches current position of SENTINEL
            if (s_matches == s_len):  # All bytes of SENTINEL matched
                out = out[:-len(SENTINEL)]  # Remove the SENTINEL from output file
                return bytearray(out)
        else:  # The byte does not match current position in the SENTINEL
            s_matches = 0  # Reset current position in the SENTINEL

    raise Exception("SENTINEL not found.")  # SENTINEL not found in the input file


# Stores the input hidden file into the input wrapper
# file using the bit method.
def bit_store(SENTINEL,offset,interval,wrapper_file,hidden_file):
    for i in range(len(hidden_file)):
        for j in range(8):
            wrapper_file[offset] &= 254
            wrapper_file[offset] |= ((hidden_file[i] & 128) >> 7)
            hidden_file[i] &= 127  # Prevents overflow, which converts the byte to an int
            hidden_file[i] <<= 1
            offset += interval

    for i in range(len(SENTINEL)):
        for j in range(8):

            wrapper_file[offset] &= 254
            wrapper_file[offset] |= ((SENTINEL[i] & 128) >> 7)
            hidden_file[i] &= 127  # Prevents overflow, which converts the byte to an int
            hidden_file[i] <<= 1
            offset += interval

    out = open(argvs["wrapper"], 'rb+')  # Opens the wrapper file to write to write changes
    out.write(wrapper_file)  # Writes the edited wrapper file
    out.close()


SENTINEL = bytearray([0x0, 0xff, 0x0, 0x0, 0xff, 0x0])  # Hardcoded sentinel values
# ---------------- Arguments initialized to default values
store_mode = False
bit_mode = False
offset = 0
interval = 1
wrapper_file = None
hidden_file = None
argvs = {}
# -----------------


parse_args()  # Parses the commandline arguments

if (bit_mode):
    if (store_mode):
        bit_store(SENTINEL, offset, interval, wrapper_file, hidden_file)
    else: # Extract mode
        sys.stdout.buffer.write(bit_extract(SENTINEL, offset, interval, wrapper_file))
else: # Byte mode
    if (store_mode):
        byte_store(SENTINEL, offset, interval, wrapper_file, hidden_file)
    else: # Extract mode
        sys.stdout.buffer.write(byte_extract(SENTINEL, offset, interval, wrapper_file))
