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
from math import radians, cos, sin, asin, sqrt


category_types = {
  '003001000000': 'Земли сельскохозяйственного назначения',
  '003002000000': 'Земли населённых пунктов',
  '003003000000': 'Земли промышленности, энергетики, транспорта, связи, радиовещания, телевидения, информатики,' +
    ' земли для обеспечения космической деятельности, земли обороны, безопасности и земли иного специального' +
    ' назначения',
  '003004000000': 'Земли особо охраняемых территорий и объектов',
  '003005000000': 'Земли лесного фонда',
  '003006000000': 'Земли водного фонда',
  '003007000000': 'Земли запаса',
  '003008000000': 'Категория не установлена',
}


def lat_long_to_GIBS(lat, lon, level):
    """
    Stable working on level = 3
    :param lat:
    :param lon:
    :param level:
    :return:
    """
    level = 7
    row = ((90 - lat) * (2 ** level)) // 288
    col = ((180 + lon) * (2 ** level)) // 288
    return row, col


def distance(lat1, lat2, lon1, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c * r)


def get_point_information_from_thermal_points(long, lat):
    # FIRST get closest city using link
    # https://nominatim.openstreetmap.org/reverse?lon=132&lat=61&addressdetails=1&limit=1&format=json
    #
    city = None
    county = None
    state = None
    distance_to_city = None
    try:
        osm_response = requests.get(
            f'https://nominatim.openstreetmap.org/reverse?lon={long}&lat={lat}&addressdetails=1&limit=1&format=json&accept-language=ru'
        )
        osm_result = osm_response.json()
        city = osm_result['address']['city']
        county = osm_result['address']['county']
        state = osm_result['address']['state']
        lat_city = osm_result['lat']
        long_city = osm_result['lon']
        # TODO Fix bug with distance
        distance_to_city = distance(lat1=lat, lat2=lat_city, lon1=long, lon2=long_city)
    except Exception as e:
        return city, county, state, distance_to_city
    return city, county, state, distance_to_city


def get_all_thermal_points_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    """
    sample query http://kaskad.ukmmchs.ru/map/query?int&20200925&20200926.json
    :param date_from:
    :param date_to:
    :return:
    """
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

        t_p, created = ThermalPoint.objects.get_or_create(
            xi=point['xi'],
            xa=point['xa'],
            yi=point['yi'],
            ya=point['ya']
        )

        # category type by API and MODEL
        land_category, fp = extract_land_category_by_geo_tag(t_p.xi, t_p.yi)
        try:
            file_name = f'{t_p.xi}{t_p.yi}'  # There's probably a better way of doing this but this is just a quick example
            t_p.satelite_image.save(file_name, files.File(fp))
        except:
            pass
        t_p.land_category = land_category
        city, county, state, distance_to_city = get_point_information_from_thermal_points(long=t_p.xi, lat=t_p.yi)
        t_p.city = city
        t_p.county = county
        t_p.state = state
        t_p.nearest_city_distance = distance_to_city
        t_p.save()


def get_all_fire_square_by_date(date_from: datetime.datetime, date_to: datetime.datetime):
    """
    url sample http://kaskad.ukmmchs.ru/map/slide?index&20200926&20200927.json
    :param date_from:
    :param date_to:
    :return:
    """
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


# TODO Fix celery cron tabs
def extract_land_category_by_geo_tag(long, lat):
    """
    Land category extraction and mapping from different sources
    :param lat:
    :param long:
    :return:
    """
    # latitude borders -90 and +90
    # longitude border -180 and +180
    # For each point i send -> https://pkk2.rosreestronline.ru/api/ll/?l=1&ll=92.852600,56.010050
    fp = None
    land_category = None
    rosreestr_response = requests.get(
        f'https://pkk2.rosreestronline.ru/api/ll/?l=1&ll={long},{lat}'
    )

    try:
        rosreestr_result = rosreestr_response.json()
        cadastr_num = rosreestr_result['features'][0]['attrs']['id']
        # Send query - https://pkk2.rosreestronline.ru/api/id/?l=1&i={cadastr number}
        # OR Get result by https://pkk.rosreestr.ru/api/features/1/50:12:0:56509
        rosreestr_2_response = requests.get(
            f'https://pkk.rosreestr.ru/api/features/1/{cadastr_num}'
        )
        rosreestr_2_result = rosreestr_2_response.json()
        land_category = rosreestr_2_result['feature']['attrs']['category_type']
    except Exception as e:
        logger.info('No result from Rosreestr')
    finally:
        pass

    try:
        row, col = lat_long_to_GIBS(lat=lat, lon=long, level=6)
        response = requests.get(
            f'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2020-05-09/250m/6/{row}/{col}.jpg'
        )
        if response.status_code == 200:
            fp = BytesIO()
            fp.write(response.content)
            #
            # TODO integrate prediction
            # Convert to torch format
            # predict
            # if land_category is None:
            #     land_category = mapp_prediction(prediction_result)
    except Exception as e:
        logger.info('No result from NASA')

    if land_category is None:
        land_category = '003008000000'

    return land_category, fp

