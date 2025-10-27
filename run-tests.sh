#!/bin/bash

source .venv/Scripts/activate

python manage.py test tests/Functional/View/ tests/Unit/Service/
