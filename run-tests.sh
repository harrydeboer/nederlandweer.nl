#!/bin/bash
if [[ ${OSTYPE} == 'msys' ]]; then
  source .venv/Scripts/activate
else
  source .venv/bin/activate
fi
python UnitTestLauncher.py
