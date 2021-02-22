import shutil
from datetime import datetime
import schedule
import time
import yaml

# Open config file
with open('serverConfig.yml') as f:  
    data = yaml.load(f, Loader=yaml.FullLoader)
    mc_folder = data.get('mc_folder')

# Zip Minecraft folder
def make_backup(dir):
    now = datetime.now()
    time = now.strftime("%Y:%m:%d_%H:%M:%S")
    fname = "serverBackups/backup "+str(time)
    shutil.make_archive(fname,'zip',dir)

# Schedule zip
schedule.every().minute.at(":00").do(make_backup, dir=mc_folder)

# Program loop
while True:
    schedule.run_pending()
    time.sleep(1)