#!/bin/bash
if [[ ${OSTYPE} == 'msys' ]]; then
  source .venv/Scripts/activate
else
  source .venv/bin/activate
fi

python manage.py test tests/Functional/View/ tests/Unit/Service/ tests/Unit/Repository tests/Unit/Model/
