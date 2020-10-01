from ftplib import FTP
from textwrap import wrap

### MAIN ###
### FTP Connect Code from Dr. Timofeyev ###
# FTP server details
IP = "138.47.99.5"
PORT = 21
USER = "anonymous"
PASSWORD = ""
METHOD = 7
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
# def formatFileList(fileList, sevenBit):
#     formattedFileList = []

#     # if using seven rightmost bits of file permissions
#     if (sevenBit):
#         # loop through file list to extract file permissions from each string in fileList
#         for file in fileList:
#             if (file[:3] == "---"):
#                 formattedFileList.append(file[3:10])
#     else:
#         pass

#     return formattedFileList

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

        # print(wrapped_content)

        for character in wrapped_content:
            int_content = int(character, 2)
            text += chr(int_content)

        return text
        

def BitDecoder(files, length):
	permissions = ""
	for f in files:
	        file_permissions = f[0:length]
	        bin_rep = ""
	        for i in file_permissions:
	                if(i == "-"):
	                        bin_rep += "0"
	                else:
	                        bin_rep += "1"
                            
	        permissions += bin_rep

	msg = ""
	for i in range(0,len(permissions),7):
	        msg += chr(int(permissions[i:i+7],2))
	return(msg)

print(BitDecoder(files, METHOD))



