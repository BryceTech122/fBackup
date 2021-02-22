from ftplib import FTP
from datetime import datetime
import schedule
import time
import yaml
import os
import logging

# Open config file
with open('clientConfig.yml') as f:  
    data = yaml.load(f, Loader=yaml.FullLoader)
    servip = data.get('server_ip')
    uname = data.get('username')
    passwd = data.get('password')
    backup_folder = data.get('backup_folder')

# Initial connect to FTP to confirm credentials
ftp = FTP(host=servip,user=uname,passwd=passwd)
ftp.close()

# Initialize logging
logging.basicConfig(filename='client.log',level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')

# Function to check if backup dir exists and if not, create one
def create_bu_dir():
    if(os.path.isdir('./backup/') == True):
        logging.info('Backup Dir Exists')
    else:
        logging.info('Creating Backup Dir')
        os.mkdir('./backup/')
        if(os.path.isdir('./backup/') == True):
            logging.info('Backup Dir Created')
        else:
            logging.info('Backup Dir Creation Failed')

# Function to copy files from budir to ./backup
def copy_backup():
    logging.info('Starting Download of All Backups')
    ftp = FTP(host=servip,user=uname,passwd=passwd)
    ftp.cwd(backup_folder)
    files = ftp.nlst()
    create_bu_dir()
    for file in files:
        logging.info('    - Downloading... '+file)
        if file.endswith('.tar'):
            ftp.retrbinary('RETR ' + file ,open('./backup/' + file, 'wb').write)
    logging.info('Done Downloading All Backups')
    ftp.close()

# Schedule backup and run at client start
schedule.every(5).minutes.at(":30").do(copy_backup)
schedule.run_all()

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)