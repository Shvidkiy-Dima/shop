#!/bin/bash


python test_connection.py --service-name mysql --port 3306  --ip mysql
python test_connection.py --service-name redis --port 6379  --ip redis
python test_connection.py --service-name memcached --port 11211  --ip memcached

cd  django_shop

python manage.py makemigrations
python manage.py migrate --fake-initial
python manage.py dockersuperuser
python manage.py collectstatic --no-input


exec gunicorn -b :8000 -w 4 --access-logfile - --error-logfile - shop.wsgi
