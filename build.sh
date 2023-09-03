#!/usr/bin/env bash
#exit of error
set -o errexit

pip install -r requirements.txt

python weaboo/manage.py collectstatic --no-input
