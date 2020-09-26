from __future__ import absolute_import, unicode_literals

from data_extractor.client.cascade import get_all_thermal_points_by_date
from FireMonitoring.celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import connection
from django.db import transaction
from django.db.utils import IntegrityError

logger = get_task_logger(__name__)


@shared_task(name="fetch_thermal_points")
def fetch_thermal_points_by_date_task() -> None:
    get_all_thermal_points_by_date(0, 0)
    logger.info('You it is task')
    return None
