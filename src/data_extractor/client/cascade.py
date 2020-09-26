import datetime
from datetime import timedelta
from django.conf import settings
import logging
from monitor.models import ThermalPoint, FireObject, FireInfo
# Get an instance of a logger
logger = logging.getLogger(__name__)
import requests
import re
from django.core.files import File  # you need this somewhere
import urllib
from django.core import files
from io import BytesIO


def get_all_thermal_points_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    _cascade_endpoint = 'http://kaskad.ukmmchs.ru/map/query?int&'

    # date_to = datetime.datetime.now().date().strftime('%Y/%m/%d')
    # date_from = datetime.datetime.now().date() - timedelta(hours=48, minutes=0)
    date_to = date_to.strftime('%Y/%m/%d')
    date_from = date_from.strftime('%Y/%m/%d')
    date_to = re.sub('[/]', '', date_to)
    date_from = re.sub('[/]', '', date_from)
    _cascade_request_url = f"{_cascade_endpoint}{date_from}&{date_to}.json"

    print(_cascade_request_url)
    response = requests.get(
        _cascade_request_url
    )
    thermal_points = response.json()
    # print(response.json())
    for point in thermal_points:
        # Predict fire type by point - month day month lat long as input
        # category type by API or MODEL
        # Save result into
        # Get meta information from OSM NOMINATIM
        t_p, created = ThermalPoint.objects.get_or_create(
            xi=point['xi'],
            xa=point['xa'],
            yi=point['yi'],
            ya=point['ya']
        )
    # sample query http://kaskad.ukmmchs.ru/map/query?int&20200925&20200926.json


def get_all_fire_square_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    _cascade_endpoint = 'http://kaskad.ukmmchs.ru/map/slide?index&'

    # date_to = datetime.datetime.now().date().strftime('%Y/%m/%d')
    # date_from = datetime.datetime.now().date() - timedelta(hours=24, minutes=0)
    date_to = date_to.strftime('%Y/%m/%d')
    date_from = date_from.strftime('%Y/%m/%d')
    date_to = re.sub('[/]', '', date_to)
    date_from = re.sub('[/]', '', date_from)
    _cascade_request_url = f"{_cascade_endpoint}{date_from}&{date_to}.json"

    print(_cascade_request_url)
    response = requests.get(
        _cascade_request_url
    )
    fire_points = response.json()
    print(response.json())
    for point in fire_points:
        fire_obj, created = FireObject.objects.get_or_create(
            x_max=point['maxx'],
            x_min=point['minx'],
            y_max=point['maxy'],
            y_min=point['miny']
        )
        if not created:
            fire_obj.x_max = point['maxx']
            fire_obj.x_min = point['minx']
            fire_obj.y_max = point['maxy']
            fire_obj.y_min = point['miny']

            image_url = f'http://kaskad.ukmmchs.ru/map/slide?slide&{point["url"]}'
            resp = requests.get(image_url)

            if resp.status_code != requests.codes.ok:
                # Error handling here
                pass
                # something wrong

            fp = BytesIO()
            fp.write(resp.content)
            file_name = image_url.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
            fire_obj.image.save(file_name, files.File(fp))
            # if image not default try
            # Smoke and fire mask prediction result
            fire_obj.save()
            thermal_points = ThermalPoint.objects.all()
            for t_p in thermal_points:
                # TODO Fix dat shit
                if (t_p.xi < fire_obj.x_max and t_p.xi > fire_obj.x_min) and (t_p.yi < fire_obj.y_max and t_p > fire_obj.y_min):
                    fir_info, created = FireInfo.objects.get_or_create(
                        thermal_point=t_p,
                        fire_obj=fire_obj,
                    )
                    if created:
                        logger.info("new fire point")

    # urls sample http://kaskad.ukmmchs.ru/map/slide?index&20200926&20200927.json

# TODO get region city by geo tag and
# TODO mapping points for fire
# TODO extract land category
# TODO Fix celery cron tabs
# TODO Fix image path for


def get_land_category_by_geo_tag():

    # For each point i send -> https://pkk2.rosreestronline.ru/api/ll/?l=1&ll=92.852600,56.010050
    # features[0][attrs][id] cadastr number
    # Send query - https://pkk2.rosreestronline.ru/api/id/?l=1&i={cadastr number}
    # OR Get result by https://pkk.rosreestr.ru/api/features/1/50:12:0:56509
    # AND MAP with
    # category_types: {
    #   '003001000000': 'Земли сельскохозяйственного назначения',
    #   '003002000000': 'Земли населённых пунктов',
    #   '003003000000': 'Земли промышленности, энергетики, транспорта, связи, радиовещания, телевидения, информатики,' +
    #     ' земли для обеспечения космической деятельности, земли обороны, безопасности и земли иного специального' +
    #     ' назначения',
    #   '003004000000': 'Земли особо охраняемых территорий и объектов',
    #   '003005000000': 'Земли лесного фонда',
    #   '003006000000': 'Земли водного фонда',
    #   '003007000000': 'Земли запаса',
    #   '003008000000': 'Категория не установлена',
    # }
    pass