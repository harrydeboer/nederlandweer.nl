#!/bin/bash
git pull origin main
source /home/deb2005684/virtualenv/dashboard_meet_je_stad/3.13/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
cp .htaccess ../public_html
