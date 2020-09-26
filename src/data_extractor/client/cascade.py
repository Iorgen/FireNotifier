import datetime
from django.conf import settings


def get_all_thermal_points_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    pass
    _cascade_url = settings.CASCADE_URL = settings.CASCADE_URL
    _cascade_endpoint = '/map/query'
    _request_url = '/'
    # Convert dates to YYYYMMDD
    # request to cascade system
    # sample query http://kaskad.ukmmchs.ru/map/query?int&20200925&20200926.json
    # save result into db


def get_all_fire_square_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    pass
    # urls sample http://kaskad.ukmmchs.ru/map/slide?index&20200926&20200927.json
    # After we get this data
    # Determine whic thermal points are inside fire square from all thermal points in our database
    # Create fire object based on thermal points
    # Also request to CASCADE for img
