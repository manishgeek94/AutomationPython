import os
import sys
import time
import glob,shutil
import smtplib
port = 25
server = "9.57.xx.xx"
mailserver = smtplib.SMTP(server, port)

# This is check current working directory
print("Current Working Directory ", os.getcwd())
# Here it will change directory to esb where all 0 priority files are there
os.chdir("/home/mdmcloud/mdmbatch/esb")

# Now - Time to check process state before kicking off the job again
processname = 'runMdmBatch.sh'
tmp = os.popen("ps -Af").read()
proccount = tmp.count(processname)
print(proccount) # give the count as 1 if process is running and up


a = os.listdir("/home/mdmcloud/mdmbatch/esb") #list all files in this current folder

def File_name_Size():
    for i in range(len(a)):
        if a[i].startswith("M"):
            print(a[i])
            size = sys.getsizeof(a[i])
            print(size)


Variable1 = File_name_Size()
print(Variable1)

time.sleep(30)

Variable2 = File_name_Size()
print(Variable2)

if Variable1 == Variable2:
    count = 0
    print("File size is not same after 30 sec so the value is",count)
else:
    count = 1
    print("File size is not same after 30 sec so the value is",count)

if count == 1:
    print("File size does not matched so we cant process files now")
    mailserver.sendmail("idm_prod@local", "manikum3@in.ibm.com", "Subject: File size does not matched so we cant process files now")

elif proccount > 0:
    print("Previous Batch job is already running,so No need to submit another batch files")
    mailserver.sendmail("idm_prod@local", "manikum3@in.ibm.com","Subject: Previous Batch job is already running,so No need to submit another batch files")

else:
    print("Script is not running so we are starting the script")

    os.chdir("/home/mdmcloud/mdmbatch/esb")
    source_dir = '/home/mdmcloud/mdmbatch/esb'  # Path where your files are at the moment
    dst = '/home/mdmcloud/mdmbatch/batch-input'  # Path you want to move your files to
    files = glob.iglob(os.path.join(source_dir, "*.txt"))
    for file in files:
        if os.path.isfile(file):
            shutil.move(file, dst)

    os.chdir("/home/mdmcloud/mdmbatch")

    os.system('./runMdmBatch.sh > runmdmbatch.log')
    open('runmdmbatch.log', 'r').read()
    print("Script started to process MDM Batch")
    mailserver.sendmail("idm_prod@local", "manikum3@in.ibm.com","Subject: Script started to process MDM Batch")


