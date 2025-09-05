#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# apply database migrations
python manage.py migrate

# create superuser if not exists
python manage.py createsuperuser --noinput || true
