from ftplib import FTP

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

# display the folder contents
for f in files:
	print(f)


def tenBitDecoder(files):
	permissions = ""
	for f in files:
	        file_permissions = f[0:10]
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
	print(msg)
