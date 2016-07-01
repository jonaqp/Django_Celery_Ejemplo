web: gunicorn django_mongo.wsgi --log-file -
scheduler: celery worker -A django_mongo -l info
