#/bin/sh
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000