#!/bin/bash

# Adjust file permissions
chmod 777 /code/auction/
chmod 666 /code/auction/uwsgi_app.sock

exec "$@"
