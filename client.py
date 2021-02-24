from ftplib import FTP
from datetime import datetime
import schedule
import time
import yaml
import os
import logging

# Initialize
def init():
    # Initialize logging
    logging.basicConfig(filename='client.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('fBackup Client Started')
    # Open hosts file and run initial connection to FTP to confirm credentials
    with open('clientHosts.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for key, value in data.items():
            ftp = FTP(host=value[0]['ip'], user=value[1]
                      ['username'], passwd=value[2]['password'])
            ftp.close()
    # Open config file and set backup times
    with open('clientConfig.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        backup_occurrence = data.get('backup_occurrence')
        backup_time = data.get('backup_time')
    # Schedule backup time
    backup = 'schedule.every().' + backup_occurrence + '.at(\'' + backup_time + '\').do(copy_backup)'
    exec(backup)
    logging.info('Init Complete!')

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
    with open('clientHosts.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        logging.info('Starting Download of All Backups')
        for key, value in data.items():
            ftp = FTP(host=value[0]['ip'], user=value[1]
                      ['username'], passwd=value[2]['password'])
            ftp.cwd(value[3]['backup_folder'])
            files = ftp.nlst()
            create_bu_dir()
            os.mkdir('./backup/'+key)
            for file in files:
                logging.info('    - Downloading... '+file)
                if file.endswith('.tar'):
                    ftp.retrbinary(
                        'RETR ' + file, open('./backup/' + key + '/' + file, 'wb').write)
            ftp.close()
        logging.info('Done Downloading All Backups')

# Initialize and set backup time and run once at program start
init()
schedule.run_all()

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)