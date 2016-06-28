import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from api.bucket import load_image
from django_mongo.celery import app

logger = get_task_logger(__name__)


@app.task
def prueba_suma(x, y):
    return x + y


@app.task
def prueba_resta(x, y):
    return x - y


@shared_task()
def fetch_url():
    scraper_example()


def scraper_example():
    logger.info("Start task")
    a = load_image()
    now = datetime.datetime.now()
    logger.info("Task finished: result = %s" % str(a))
