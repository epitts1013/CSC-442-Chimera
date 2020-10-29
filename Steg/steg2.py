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
            wrapper_file = bytearray(open(arg[2:],'rb').read())
        elif(arg_h == '-h'):
            hidden_file = bytearray(open(arg[2:],'rb').read())

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
    
    s_matches = 0
    s_len = len(sentinel)
    out = bytearray()
    
    while(offset < len(wrapper_file)):
        byte = wrapper_file[offset]
        if(byte == sentinel[s_matches]):
            s_matches += 1
            if(s_matches >= s_len):
                #for byte in sentinel:
                #    out.append(byte)
                #print(out)
                return out
                break
        else:
            s_matches = 0
            out.append(byte)
            
        offset += interval
    return(None)

def bit_extract():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file

    s_matches = 0
    s_len = len(sentinel)
    out = bytearray()
    
    while(offset < len(wrapper_file)-(interval*8)):
        byte = 0
        for j in range(8):
            byte |= (wrapper_file[offset] & 1)
            if(j < 7):
                byte <<= 1
                offset += interval
        if(byte == sentinel[s_matches]):
            s_matches += 1
            if(s_matches >= s_len):
                for byte in sentinel:
                    out.append(byte)
                return out
        else:
            s_matches = 0
            out.append(byte)
    return None
    

def bit_store():
    global sentinel
    global store_mode
    global bit_mode
    global offset
    global interval
    global wrapper_file
    global hidden_file

    for i in range(len(hidden_file)):
        for j in range(8):
            wrapper_file[offset] &= 254
            wrapper_file[offset] |= ((hidden_file[i] & 128) >> 7)
            hidden_file[i] <<= 1
            offset += interval
    for i in range(len(sentinel)):
        for j in range(8):
            wrapper_file[offset] &= 254
            wrapper_file[offset] |= ((sentinel[i] & 128) >> 7)
            sentinel[i] <<= 1
            offset += interval

sentinel = bytearray([0x0,0xff,0x0,0x0,0xff,0x0])
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
        if(store_mode):
            ""
        else:
            sys.stdout.buffer.write(bit_extract())
    else:
        if(store_mode):
            ""
        else:
            sys.stdout.buffer.write(byte_extract())


"""
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
"""
