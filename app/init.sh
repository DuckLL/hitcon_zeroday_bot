#!/bin/sh

cd /app
pip install -r requirements.txt
python3 /app/bot.py
cp ./crontab /etc/crontab
/sbin/my_init
