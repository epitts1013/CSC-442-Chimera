from ftplib import FTP
from textwrap import wrap

### MAIN ###
### FTP Connect Code from Dr. Timofeyev ###
# FTP server details
IP = "138.47.99.5"
PORT = 21
USER = "anonymous"
PASSWORD = ""
METHOD = 10
FOLDER = "/" + str(METHOD) + "/"
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
# take in the list of files and output 
def formatFileList(fileList, length):
    formattedFileList = []

    # if using seven rightmost bits of file permissions
    if (length == 7):
        # loop through file list to extract file permissions from each string in fileList
        for file in fileList:
            if (file[:3] == "---"):
                formattedFileList.append(file[3:10])
    else:
        for file in fileList:
            formattedFileList.append(file[:10])

    return formattedFileList

# decodes message encoded in file permissions
def convertToBitString(filePermissions):
    textString = "".join(filePermissions)
    bits = []

    for char in textString:
        if (char == "-"):
            bits.append("0")
        else:
            bits.append("1")

    return "".join(bits)


def binaryConvert(content, length):
    text = ""

    if (len(content) % length) == 0: 

        wrapped_content = wrap(content, length)

        for character in wrapped_content:
            int_content = int(character, 2)
            text += chr(int_content)

        return (text)

# set code to be executed based on whether we are looking in the /7/ directory
print(binaryConvert(convertToBitString(formatFileList(files, METHOD)), 7))

