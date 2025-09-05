#!/usr/bin/env bash
# exit on error
set -o errexit

# If manage.py is at repo root (e.g., SIH-MAIN-3), run here.
if [ -f "manage.py" ]; then
  pip install -r requirements.txt
  python manage.py collectstatic --no-input
  python manage.py migrate
  exit 0
fi

# Otherwise, assume monorepo layout with sih-main-3/ (e.g., SIH-MAIN)
if [ -d "sih-main-3" ]; then
  cd sih-main-3
  pip install -r requirements.txt
  python manage.py collectstatic --no-input
  python manage.py migrate
  exit 0
fi

echo "Could not find manage.py or sih-main-3 directory" >&2
exit 1

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
