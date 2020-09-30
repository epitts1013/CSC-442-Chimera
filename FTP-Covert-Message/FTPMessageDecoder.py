from ftplib import FTP

### METHODS ###
def formatFileList(fileList, sevenBit):
    formattedFileList = []

    # if using seven rightmost bits of file permissions
    if (sevenBit):
        # loop through file list to extract file permissions from each string in fileList
        for file in fileList:
            if (file[:3] == "---"):
                formattedFileList.append(file[3:10])
    else:
        pass

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

### MAIN ###
### FTP Connect Code from Dr. Timofeyev ###
# FTP server details
IP = "138.47.99.5"
PORT = 21
USER = "anonymous"
PASSWORD = ""
FOLDER = "/7/"
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

# for file in files:
#     print(file)

# set code to be executed based on whether we are looking in the /7/ directory
if (FOLDER == "/7/"):
    bitString = convertToBitString(formatFileList(files, True))
    print(bitString)
elif (FOLDER == "/10/"):
    pass