#!/bin/bash

if [[ ${OSTYPE} == 'msys' ]]; then
  source .venv/Scripts/activate
else
  source .venv/bin/activate
fi

python manage.py test tests/Functional/Command/ tests/Functional/Form/ tests/Functional/Repository/ tests/Functional/Service/ tests/Functional/View/ tests/Unit/File/ tests/Unit/Form/
