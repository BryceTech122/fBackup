from ftplib import FTP
from datetime import datetime
import schedule
import time
import yaml

# Open config file
with open('clientConfig.yml') as f:  
    data = yaml.load(f, Loader=yaml.FullLoader)
    servip = data.get('server_ip')
    uname = data.get('username')
    passwd = data.get('password')
    budir = data.get('backup_folder')

# Connect to ftp
ftp = FTP(host=servip,user=uname,passwd=passwd)
ftp.cwd(budir)

# Copy files to local directory
def copy_backup():
    files = ftp.nlst()
    for file in files:
        print("Downloading "+file)
        ftp.retrbinary("RETR " + file ,open("./backups" + file, 'wb').write)
    ftp.close()

# Schedule backup
schedule.every().minute.at(":30").do(copy_backup)

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)