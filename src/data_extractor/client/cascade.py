import datetime
from datetime import timedelta
from django.conf import settings
import logging
from monitor.models import ThermalPoint, FireObject, FireInfo
# Get an instance of a logger
logger = logging.getLogger(__name__)
import requests
import re


def get_all_thermal_points_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    _cascade_endpoint = 'http://kaskad.ukmmchs.ru/map/query?int&'

    date_to = datetime.date.today().strftime('%Y%MM%DD')
    date_from = datetime.datetime.now() - timedelta(hours=24, minutes=0)
    date_from = date_from.strftime('%Y%M%D')
    line = re.sub('[/]', '', date_from)
    _cascade_request_url = f"{_cascade_endpoint}{date_from}&{date_to}.json"

    print(_cascade_request_url)
    response = requests.get(
        _cascade_request_url
    )
    logger.info(response.json())
    # sample query http://kaskad.ukmmchs.ru/map/query?int&20200925&20200926.json


def get_all_fire_square_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    _cascade_endpoint = 'ttp://kaskad.ukmmchs.ru/map/slide?index&'

    date_to = datetime.datetime.now().strftime('%YYYY%MM%DD')
    date_from = datetime.datetime.now() - timedelta(hours=24, minutes=0)
    date_from = date_from.strftime('%YYYY%MM%DD')
    _cascade_request_url = f"{_cascade_endpoint}{date_from}&{date_to}.json"
    response = requests.get(
        _cascade_request_url
    )
    logger.info(response.json())
    # objects.get_or_create(
    # urls sample http://kaskad.ukmmchs.ru/map/slide?index&20200926&20200927.json
    # Select
    # After we get this data
    # Determine whic thermal points are inside fire square from all thermal points in our database
    # Create fire object based on thermal points
    # Also request to CASCADE for img


def get_land_category_by_geo_tag():
    pass