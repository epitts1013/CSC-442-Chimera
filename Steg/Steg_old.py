# IMPORTS
from sys import argv

# VARIABLES
offset = 0          # number of bytes from start of wrapper file that hidden file starts
interval = 1        # interval between hidden file bytes
process = ""        # store or retrieve mode
mode = ""           # bit or byte mode
wrapperFile = ""    # File that hidden file is stored in
hiddenFile = ""     # File to be hidden in wrapperFile

# METHODS
def StoreHiddenFile(offset, interval, mode, wrapperFile, hiddenFile):
    pass

def RetrieveHiddenFile(offset, interval, mode, wrapperFile):
    pass

# MAIN
# get variables from command line arguments
for arg in argv:
    # get first two characters of argument   
    argSlice = arg[:2]

    # process argument
    if (argSlice == "-s"):      # argument for setting to store mode
        process = "s"
    elif (argSlice == "-r"):    # argument for setting to retrieve mode
        process = "r"
    elif (argSlice == "-b"):    # argument for setting to bit mode
        mode = "bit"
    elif (argSlice == "-B"):    # argument for setting to byte mode
        mode = "byte"
    elif (argSlice == "-o"):    # argument for setting offset size
        offset = int(arg[2:])   
    elif (argSlice == "-i"):    # argument for setting interval size
        interval = int(arg[2:]) 
    elif (argSlice == "-w"):    # argument for setting wrapper file path
        wrapperFile = arg[2:]
    elif (argSlice == "-h"):    # argument for setting hidden file path
        hiddenFile = arg[2:]

# call method based on process
if (process == "s"):
    StoreHiddenFile(offset, interval, mode, wrapperFile, hiddenFile)
elif (process == "r"):
    RetrieveHiddenFile(offset, interval, mode, wrapperFile)