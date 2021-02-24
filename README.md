# Folder Backup

## Prerequisites
This guide assumes that you have a ftp server Installed on your server like vsftpd. It also assumes you are familiar with git, github, and python

## Overview
To install fBackup you must clone the repo to your server and the server in which the backups will be stored. On your source server there must be a ftp server to host all the backup files and then the client will connect to the ftp directory and clone them to a local directory.

## Install Server
### Clone repo and move to /etc/
```bash
sudo git clone https://github.com/BryceTech122/fBackup
sudo mv ./fBackup /etc/fBackup
```

### Edit serverConfig.yml
```bash
cd /etc/fBackup
sudo nano ./serverConfig.yml
```
Put your folder to be backed up between the quotes and adjust backup frequency if needed, default is once a day at midnight. NOTE: Server and Client backup frequencies should be the same or data loss is possible.
```json
mc_folder: '/etc/spigot/'
backup_occurrence: 'day'
backup_time: '00:00'
```

### Install Python, Pip and Requirements
```bash
sudo apt-get install python3 python3-pip -y
sudo pip3 install -r ./requirements.txt
```
### Create systemd service
```bash
sudo nano /etc/systemd/system/fBackup.service
```
```
[Unit]
Description=fBackup-server
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 ./server.py
WorkingDirectory=/etc/fBackup/

[Install]
WantedBy=multi-user.target
```
### Start and Enable systemd service
```bash
sudo systemctl start fBackup.service
sudo systemctl enable fBackup.service
sudo systemctl status fBackup.service
```
### Install vsftpd
```bash
sudo apt-get install vsftpd
```
### Enable and start vsftpd
```bash
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo systemctl status vsftpd
```

## Install on Client
### Clone repo and move to /etc/
```bash
sudo git clone https://github.com/BryceTech122/fBackup
sudo mv ./fBackup /etc/fBackup
```

### Edit clientHosts.yml
```bash
cd /etc/fBackup
sudo nano ./clientHosts.yml
```
This is your hosts file where you define which servers to be backed up and their respective credentials. Fill in your FTP server IP / Hostname, user and password, if you have multiple servers copy the template and repeat, if not remove everything but what you need. For backup_folder put in the directory where your backups are stored on the server, if you have not changed it it will be in your working directory under the "backup" directory
```json
server1:
    - ip: ''
    - username: ''
    - password: ''
    - backup_folder: '/etc/fBackup/backup'

server2:
    - ip: ''
    - username: ''
    - password: ''
    - backup_folder: '/etc/fBackup/backup'
```

### Edit clientConfig.yml
Use this file to set how often you want backups to occur, either once a minute, hour, or day. Options for backup_occurrence is case specific. To set a time in which the backups should be started edit the backup_time setting. If your backup_occurrence is set to day use HH:MM or HH:MM:SS formatting, if backup_occurrence is set hour use :MM formatting or if it is set to minute use :SS formatting. Default is set to once a day at midnight, for more information on scheduling please visit schedule.readthedocs.io
```json
backup_occurrence: 'day'
backup_time: '00:00'
```

### Install Python, Pip and Requirements
```bash
sudo apt-get install python3 python3-pip -y
sudo pip3 install -r ./requirements.txt
```
### Create systemd service
```bash
sudo nano /etc/systemd/system/fBackup.service
```
```
[Unit]
Description=fBackup-client
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 ./client.py
WorkingDirectory=/etc/fBackup/

[Install]
WantedBy=multi-user.target
```
### Start and Enable systemd service
```bash
sudo systemctl start fBackup.service
sudo systemctl enable fBackup.service
sudo systemctl status fBackup.service
```