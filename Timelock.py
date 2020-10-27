from sys import stdin 
from datetime import datetime
import pytz
from hashlib import md5

DEBUG = True

ON_SERVER = False

Time_Interval = 60
Manual_Date_Time = ""

Epoch = stdin.read().rstrip("\n")

#Automatically gets current time if Manual_Date_Time is empty
if Manual_Date_Time == "":
	Current_Time = datetime.now()
	Current_Time = datetime.strftime(Current_Time,"%Y %m %d %H %M %S")
	Current_Time = datetime.strptime(Current_Time,"%Y %m %d %H %M %S")
else:
	Current_Time = Manual_Date_Time
	Current_Time = datetime.strptime(Current_Time,"%Y %m %d %H %M %S")

#Sets the local timezone to Central
local_time = pytz.timezone("America/Chicago")

#Sets Current_Time and Epoch to Datetime objects
Epoch = datetime.strptime(Epoch,"%Y-%m-%d %H:%M:%S")

#Sets the timezone of both times to Central
Current_Time = local_time.localize(Current_Time, is_dst=None)
Epoch = local_time.localize(Epoch, is_dst=None)

#Converts both times to UTC
Current_Time = Current_Time.astimezone(pytz.utc)
Epoch = Epoch.astimezone(pytz.utc)

#Gets the amount of seconds between the two dates
Difference = int((Current_Time - Epoch).total_seconds())
old_Difference = Difference
#Gets the Time Interval of the time difference
while (Difference%Time_Interval) != 0:
	Difference -= 1  

#Creates a MD5 hash based on the difference in seconds between the two dates that is hashed again
MD5_hash = md5(str(Difference)).hexdigest()
MD5_hash2 = md5(MD5_hash).hexdigest()

#Sets code to an empty string 
Code = ""

#Adds the first 2 letters of the MD5 hash to the code
i = 0
k = 0
while i < len(MD5_hash2):
	if MD5_hash2[i].islower() == True and k < 2:
		Code += MD5_hash2[i]
		k +=1
	i += 1

#Adds the first 2 numbers starting from the end of the MD5 hash to the code
i = 0
j = 0
while i < len(MD5_hash2):
	if MD5_hash2[(len(MD5_hash2)-1)-i].isdigit() == True and j < 2:
		Code += MD5_hash2[(len(MD5_hash2)-1) - i]
		j +=1
	i +=1
Code += MD5_hash2[(len(MD5_hash2)/2)]
#Debug
if DEBUG == True:
	print ("Current (UTC): {}".format(Current_Time))
	print ("Epoch (UTC): {}".format(Epoch))
	print ("Seconds: {}".format(old_Difference))
	print ("Seconds: {}".format(Difference))
	print ("MD5 #1: {}".format(MD5_hash))
	print ("MDF #2: {}".format(MD5_hash2))
#Prints out the code
print ("Code: {}".format(Code))
