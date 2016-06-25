import datetime

from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from celery import shared_task
from django_mongo.celery import app
from api.bucket import load_image
logger = get_task_logger(__name__)


@app.task
def prueba_suma(x, y):
    return x + y


@app.task
def prueba_resta(x, y):
    return x - y


@app.task
def enviar_mail(asunto, contenido, destinatario):
    send_mail(asunto, contenido, 'noreply@mail.com', [destinatario], fail_silently=False)


@shared_task()
def fetch_url():
    scraper_example()


def scraper_example():
    logger.info("Start task")
    a = load_image()
    now = datetime.datetime.now()
    logger.info("Task finished: result = %s" % str(a))
