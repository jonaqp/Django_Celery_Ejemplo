from celery import shared_task
from celery.utils.log import get_task_logger

from api.bucket import load_image

logger = get_task_logger(__name__)



@shared_task()
def task_load_database():
    general_function_bucket()


def general_function_bucket():
    logger.info("Start task")
    a = load_image()
    logger.info("Task finished: result = %s" % str(a))
