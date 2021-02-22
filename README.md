# Minecraft Backup

## Prerequisites
This guide assumes that you have a ftp server Installed on your Minecraft server like vsftpd. It also assumes you are familiar with git, github, and python

## Overview
To install mcBackup you must clone the repo to your minecraft server and the server in which the backups will be stored. On your minecraft server there must be a ftp server to host all the backup files and then the client will connect to the ftp directory and clone them to a local directory.

## Install Server
### Clone repo and move to /etc/
```bash
sudo git clone https://github.com/BryceTech122/mcBackup
sudo mv ./mcBackup /etc/mcBackup
```

### Edit serverConfig.yml
```bash
cd /etc/mcBackup
sudo nano ./serverConfig.yml
```
Put your minecraft server folder between the quotes
```bash
mc_folder: '/etc/spigot/'
```

### Install Python, Pip and Requirements
```bash
sudo apt-get install python3 python3-pip -y
sudo pip3 install -r ./requirements.txt
```
### Create systemd service
```bash
sudo nano /etc/systemd/system/mcbackup.service
```
```
[Unit]
Description=mcBackup-server
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 ./server.py
WorkingDirectory=/etc/mcBackup/

[Install]
WantedBy=multi-user.target
```
### Start and Enable systemd service
```bash
sudo systemctl start mcbackup.service
sudo systemctl enable mcbackup.service
sudo systemctl status mcbackup.service
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
sudo git clone https://github.com/BryceTech122/mcBackup
sudo mv ./mcBackup /etc/mcBackup
```

### Edit clientConfig.yml
```bash
cd /etc/mcBackup
sudo nano ./clientConfig.yml
```
Fill in your FTP server IP / Hostname, user and password. For backup_folder put in the directory where your backups are stored on the server, if you have not changed it it will be in your working directory under the "backup" directory
```bash
server_ip: '' #FTP Server IP
username: '' #FTP Server Username
password: '' #FTP Server Password
backup_folder: '/etc/mcBackup/backup' #FTP Server Backup Location
```

### Install Python, Pip and Requirements
```bash
sudo apt-get install python3 python3-pip -y
sudo pip3 install -r ./requirements.txt
```
### Create systemd service
```bash
sudo nano /etc/systemd/system/mcbackup.service
```
```
[Unit]
Description=mcBackup-client
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 ./client.py
WorkingDirectory=/etc/mcBackup/

[Install]
WantedBy=multi-user.target
```
### Start and Enable systemd service
```bash
sudo systemctl start mcbackup.service
sudo systemctl enable mcbackup.service
sudo systemctl status mcbackup.service
```