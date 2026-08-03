#!/bin/bash
git pull origin master
source .venv/bin/activate
python manage.py migrate
pip install -r requirements.txt
service gunicorn restart
