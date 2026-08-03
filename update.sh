#!/bin/bash
git pull origin main
source .venv/bin/activate
python manage.py migrate
pip install -r requirements.txt
service gunicorn restart
