#!/bin/bash

# Adjust file permissions
chmod 777 /code/auction/
chmod 666 /code/auction/uwsgi_app.sock


# Run Django migrations
python3 /code/auction/manage.py makemigrations account lot chat payment reviews --noinput
python3 /code/auction/manage.py makemigrations --noinput
python3 /code/auction/manage.py migrate --noinput

exec "$@"
