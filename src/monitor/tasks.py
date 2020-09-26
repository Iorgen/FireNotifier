from __future__ import absolute_import, unicode_literals

from data_extractor.client.cascade import (
    get_all_thermal_points_by_date,
    get_all_fire_square_by_date
)
import datetime
from FireMonitoring.celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import connection
from django.db import transaction
from django.db.utils import IntegrityError

logger = get_task_logger(__name__)


@shared_task(name="fetch_thermal_points")
def fetch_thermal_points_by_date_task() -> None:
    date_from = datetime.datetime(2020, 6, 25)
    # THIS date is dummy and does not mean anything )_)())
    date_to = datetime.datetime(2020, 6, 26)
    get_all_thermal_points_by_date(date_from,date_to)
    logger.info('You it is task')
    return None


@shared_task(name="fetch_fire_square")
def fetch_fire_squares_by_date_task() -> None:

    get_all_fire_square_by_date(datetime.datetime(2020, 6, 25), datetime.datetime(2020, 6, 26))
    logger.info('You it is task')
    return None
