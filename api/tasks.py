from celery import shared_task
from celery.utils.log import get_task_logger

from api.bucket import load_image

logger = get_task_logger(__name__)



@shared_task()
def fetch_url():
    scraper_example()


def scraper_example():
    logger.info("Start task")
    a = load_image()
    logger.info("Task finished: result = %s" % str(a))
