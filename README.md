##FYP
Date to be completed: 2024-03-20

# Credentials

## Admin

Email: admin@gmail.com
Password: admin

## Test User

Email: dhanbdrkarki111@gmail.com
Password: P@ssword0

# Social Authentication: Google

## To enable, social auth:

1. Goto C:\Windows\System32\drivers\etc
2. Add line: 127.0.0.1 bidme.com

## only can run social auth with this command:

python manage.py runserver_plus --cert-file cert.crt

# Run docker

docker run -it --name redis -p 6379:6379 redis
