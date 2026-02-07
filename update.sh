#!/bin/bash
set -e

if [[ $EUID -eq 0 ]]; then
  echo "This script must NOT be run as root" 1>&2
  exit 1
fi
git pull origin master
source .venv/bin/activate
python manage.py migrate
pip install -r requirements.txt
service gunicorn restart