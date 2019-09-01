# Test blog
Django based web application with following functionality:
1. Login/Registration.
2. Connected django admin interface.
3. Functionality for Post: create, update, read, delete.
4. Functionality for Comment: create, read.
5. Email notifications.

Technologies:
1. Python/Django.
2. MySQL storage.
4. Celery for send email in background.
5. Redis as broker for celery.
6. Docker, docker-compose

## Usage

Create dev/setting_local.py with following config:
1. SECRET_KEY
2. DEBUG
3. EMAIL_USER_TLS
4. EMAIL_HOST
5. EMAIL_HOST_USER
6. EMAIL_HOST_PASSWORD
7. EMAIL_PORT

### Run application locally

Build project:
```bash
docker-compose build
```

Bring up only `db` container and await loading image and creation local db:
```bash
docker-compose up db
CTRL+С
```

Bring up whole services:
```bash
docker-compose up
```

Run migrations:
```bash
docker-compose exec web python manage.py migrate
```