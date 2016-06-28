web: gunicorn django_mongo.wsgi --log-file -
scheduler: celery worker -B -A django_mongo -l info
