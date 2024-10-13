# Final Year Project

## Introduction

Online auction and bidding system is a revolutionary digital commerce innovation that offers a user-centric platform for seamless bidding experiences. It functions as a virtual marketplace, connecting buyers and sellers through a transparent exchange process. The platform serves as a centralized hub, showcasing a diverse array of goods and catering to a broad spectrum of consumer interests. It efficiently coordinates the exchange of information between buyers and sellers, creating a lively market. Sellers can curate their offerings with detailed listings, while registered users can bid on items, they want.

### Objectives

- To develop a user-friendly online web-based auction system that can be accessed by prospective auctioneers and dealers anywhere in the world.
- To provide an efficient and effective bidding process with real-time updates on bidding status.
- To enhance the user experience by enabling communication between users through a built-in messaging system.
- To implement secure authentication and authorization and integrate different payment options within the platform.

### Deliverables

- User-Friendly Interface: Designed for quick navigation and easy access to all functions.
- Secure Transactions: Integrates popular payment gateways like ESewa and Khalti for secure financial transactions.
- Real-Time Bidding: Supports instant outbid notifications and dynamic environment for quick reactions.
- Comprehensive Item Listings: Provides high-quality images, descriptions, and context for informed decision-making.
- Communication: Provides embedded messaging facilities for effective communication between buyers and sellers.
- Transparency: Displays complete auction listings for fair competition and decision-making.
- Rating and Feedback System: Allows users to rate their experiences and leave feedback post-transaction.
- Advanced Search and Discovery: Provides a powerful search engine and filtering options for easy item location.
- Mobile Accessibility: Designed for convenient access from smartphones and tablets.

## Prerequisites

- Basic knowledge on Python, Django, DRF, Postgres, Docker
- Must install Docker, Python, PgAdmin (for Postgres database)

## Running Application

### Virtual Environment Setup

```
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd auction
py manage.py runserver
```

### Update .env file as per your need

```
DJANGO_SECRET_KEY = '<DJANGO SECRET KEY HERE>'
EMAIL_HOST_USER = '<EMAIL FOR SENDING MAIL>'
EMAIL_HOST_PASSWORD = '<EMAIL PASSWORD>'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<GOOGLE OAUTH2 KEY FOR GOOGLE AUTHENTICATION>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<GOOGLE OAUTH2 SECRET FOR GOOGLE AUTHENTICATION>'

DB_NAME = '<DATABASE NAME>'
DB_USER = '<DATABASE USERNAME>'
DB_PASSWORD = '<DATABASE PASSWORD>'


# KHALTI Authorization Key
KHALTI_AUTHORIZATION_KEY = 'KHALTI AUTHORIZATION KEY FOR PAYMENT INTEGRATION'
```

### Setup docker container

#### Run redis

```
docker run -it --name redis -p 6379:6379 redis
```

### Run rabbitmq for message queuing

```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:management
```

### Run celery for consuming message

```
celery -A auction worker --loglevel=INFO --pool=solo
```

Here, RabbitMQ run on port 5672, and its web-based
management user interface on port 15672.

### OR, Flower (Optional)

celery -A auction flower
url: http://localhost:5555/

### Google Social Authentication (Optional)

To add social authentication,
console: https://console.cloud.google.com/
Doc: https://developers.google.com/identity/protocols/OAuth2

Then go to api and services for setup.

Next,

1. Goto C:\Windows\System32\drivers\etc
2. Add line: `127.0.0.1 bidme.com`

Then, run application with this command:

python manage.py runserver_plus --cert-file cert.crt
or
python manage.py runserver_plus 8001 --cert-file cert.crt

Note: You can only sign up or login using the email you have added in the developer console of google for social authentication.
