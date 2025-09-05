#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# apply database migrations
python manage.py migrate

# create superuser (set your username, email, and password here)
export DJANGO_SUPERUSER_USERNAME=shubhamjh4
#export DJANGO_SUPERUSER_EMAIL=rockshubham.e12@gmail.com
export DJANGO_SUPERUSER_PASSWORD=admin   # 👈 must be set

python manage.py createsuperuser --noinput || true
