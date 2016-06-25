web: gunicorn django_mongo.wsgi --log-file -
worker: python manage.py celery worker --loglevel=info
celery_beat: python manage.py celery beat --loglevel=info