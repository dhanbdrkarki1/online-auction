## FYP Deployment: Online Auction Application
A containerized online auction application using Docker Compose.

## Prerequisites
- Docker Engine 20.10.x or later
- Docker Compose V2 or later
- Git

## Application Architecture
The application consists of the following services:
- Web Application (Django)
- Redis (Cache & Session Store)
- RabbitMQ (Message Broker)
- Celery (Async Task Processing)
- PostgreSQL (Database)

## Getting Started
1. Clone the Repository
```
git clone https://github.com/dhanbdrkarki1/online-auction.git
cd online-auction
```

2. Required Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
DJANGO_SECRET_KEY=your_secure_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=auction.settings.prod

# Django Super User
DJANGO_SUPERUSER_USERNAME=your_django_superuser_name
DJANGO_SUPERUSER_PASSWORD=your_django_superuser_password
DJANGO_SUPERUSER_EMAIL=your_django_superuser_email

# Database Configuration
DB_NAME=auction_db
DB_USER=auction_admin
DB_PASSWORD=auction_admin
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# RabbitMQ Configuration
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_INTERFACE_PORT=15672

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_specific_password

# Social Authentication
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

3. Starting the application
```
docker compose up -d --build
```

## Accessing the Website
Browse this link:
```
http://localhost
```

For Admin Page,
```
http://localhost/admin
```

### RabbitMQ Management Interface
Access: http://localhost:15672

Default credentials: guest/guest

## SSL Configuration (Optional)
Generate SSL certificates for HTTPS:
```
openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
-keyout ssl/bidme.key -out ssl/bidme.crt \
-subj '/CN=*.bidme.com' \
-addext 'subjectAltName=DNS:*.bidme.com'
```


## Social Authentication: Google (Optional)

## To enable, social auth:

In windows,
1. Goto C:\Windows\System32\drivers\etc (in Windows) or Goto /etc/hosts (in linux)
2. Add line: 127.0.0.1 bidme.com

3. Configure Google OAuth:
    - Go to Google Cloud Console
    - Create OAuth 2.0 credentials
    - Add authorized redirect URIs
    - Update GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env


## View Logs
```
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f <service-name>
```

### Deleting services
```
docker compose down
```