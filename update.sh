#!/bin/bash
git pull origin master
source .venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
service gunicorn restart
