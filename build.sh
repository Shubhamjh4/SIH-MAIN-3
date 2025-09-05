#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# apply database migrations
python manage.py migrate

# create superuser (set your username, email, and password here)
export DJANGO_SUPERUSER_USERNAME=rajan
export DJANGO_SUPERUSER_EMAIL=rajan@123
# export DJANGO_SUPERUSER_PASSWORD=yourpassword   # 👈 must be set

python manage.py createsuperuser --noinput || true
