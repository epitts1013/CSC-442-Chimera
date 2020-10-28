import sys

def parse_args():
    args = sys.argv[1:]
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file
    for arg in args:
        arg_h = arg[0:2]
        if(arg_h == '-s'):
            store_mode = True
        elif(arg_h == '-r'):
            store_mode = False
        elif(arg_h == '-b'):
            bit_mode = True
        elif(arg_h == '-B'):
            bit_mode = False
        elif(arg_h == '-o'):
            offset = int(arg[2:])
        elif(arg_h == '-i'):
            interval = int(arg[2:])
        elif(arg_h == '-w'):
            wrapper_file = open(arg[2:],'rb').read()
        elif(arg_h == '-h'):
            hidden_file = open(arg[2:],'rb').read()

def byte_optimal_interval():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file
    return(int((len(wrapper_file)-offset)/(len(hidden_file)-sentinel)))
    
def byte_store():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file

    for i in range(len(hidden_file)):
        wrapper_file[offset] = hidden_file[i]
        offset += interval
        
    for i in range(len(sentinel)):
        wrapper_file[offset] = sentinel[i]
        offset += interval

def byte_extract():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file
    sentinel_matches = []
    out = []
    while(offset < len(wrapper_file)):
        byte = wrapper_file[offset]
        if(len(sentinel_matches) > 0):
            #print(byte)
            if(sentinel[len(sentinel_matches)+1] == byte):
                sentinel_matches.append(byte)
                if(len(sentinel)==len(sentinel_matches)):
                    for b in sentinel_matches:
                        out.append(byte)
                    return(out)
            else:
                #print("!MATCH",byte)
                for byte in sentinel_matches:
                    out.append(byte)
                sentinel_matches = []
        elif(byte == sentinel[0]):
            #print(byte)
            sentinel_matches.append(byte)
            if(len(sentinel) == 1):
                break
        else:
            out.append(byte)
        offset += interval
    return(out)

def bit_extract():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file
    

def bit_store():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file


sentinel = [0x0,0xff,0x0,0x0,0xff,0x0]
#---------------- Arguements
store_mode = False
bit_mode = False
offset = 0
interval = 1
wrapper_file = None
hidden_file = None
#-----------------


if __name__ == '__main__':
    parse_args()
    
    if(bit_mode):
        ""
    else:
        if(store_mode):
            ""
        else:
            sys.stdout.buffer.write(bytearray(byte_extract()))
            #byte_extract()

