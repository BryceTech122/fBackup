import shutil
from datetime import datetime
import schedule
import time
import yaml
import os.path
import os
import tarfile

# Open config file
with open('serverConfig.yml') as f:  
    data = yaml.load(f, Loader=yaml.FullLoader)
    source_dir = data.get('mc_folder')

# Function to get current time for logging
def current_time():
    now = datetime.now()
    time = now.strftime('%Y:%m:%d_%H:%M:%S')
    return time

# Function to generate filename with .tar extenssion
def make_filename():
    now = datetime.now()
    time = now.strftime("%Y:%m:%d_%H:%M:%S")
    fname = "backups/backup_"+str(time)+'.tar'
    return fname

# Function to remove old backups
def remove_old(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.tar'):
            os.remove(folder_path + file_name)

# Function to tarfile your source_dir
def make_tarfile(source_dir):
    print('['+current_time()+'] Starting Backup')
    remove_old('./backups/')
    print('['+current_time()+'] Removing Previous Backups')
    output_filename = make_filename()
    with tarfile.open(output_filename, "w:gz") as tar:
        print('['+current_time()+'] Starting Backup '+output_filename)
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    print('['+current_time()+'] Backup Complete! '+output_filename)

# Schedule zip
schedule.every(5).minutes.at(":00").do(make_tarfile, source_dir=source_dir)

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)
