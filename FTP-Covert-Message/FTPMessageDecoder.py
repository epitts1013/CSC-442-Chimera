from ftplib import FTP
from textwrap import wrap

# FTP server details
IP = "138.47.99.29"
PORT = 8008
USER = "valkyrie"
PASSWORD = "myfirstchallenge"
METHOD = 7
FOLDER = "/home/valkyrie/.secretstorage/.folder2/.howaboutonemore/"
USE_PASSIVE = True # set to False if the connection times out

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []
ftp.dir(files.append)

# exit the FTP server
ftp.quit()

### METHODS ###

# binary to ascii
def binaryConvert(content, length = 7):
    text = ""

    if (len(content) % length) == 0: 

        wrapped_content = wrap(content, length)

        for character in wrapped_content:
            int_content = int(character, 2)
            text += chr(int_content)

        return (text)

# decodes message encoded in file permissions
def convertToBitString(filePermissions):
    textString = "".join(filePermissions)
    bits = []

    # Replace each dash with a zero, anything else is replaced by a one
    for char in textString:
        if (char == "-"):
            bits.append("0")
        else:
            bits.append("1")

    return "".join(bits)

# take in the list of files and output 
def formatFileList(fileList, length):
    formattedFileList = []

    # if using seven rightmost bits of file permissions
    if (length == 7):
        # loop through file list to extract file permissions from each string in fileList
        for file in fileList:

            # Ignoring files with noise in the first three characters
            if (file[:3] == "---"):
                formattedFileList.append(file[3:10])

    elif(length == 10):
        # This is currently checking for 10bits
        for file in fileList:
            formattedFileList.append(file[:10])

    else: 
        pass
    
    return formattedFileList

# set code to be executed based on the defined directory
print(binaryConvert(convertToBitString(formatFileList(files, 7))))
print(binaryConvert(convertToBitString(formatFileList(files, 10))))
