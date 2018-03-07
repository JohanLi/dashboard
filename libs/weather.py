import requests
from datetime import datetime, timedelta
from collections import OrderedDict
from lxml import etree
from libs import cache


def get_weather(bust_cache=False):
    if bust_cache:
        weather = {}
    else:
        weather = cache.get('weather') or {}

    if not weather:
        weather = {
            'sun': {},
            'forecast': [],
            'forecast_hour': [],
        }

        response = requests.get(
            'https://www.yr.no/place/Sweden/Stockholm/Stockholm/forecast.xml',
            headers={
                'user-agent': 'johanli.com',
            },
        )

        forecast_xml = etree.fromstring(response.content)

        sun = forecast_xml.xpath('sun')[0]

        weather['sun'] = {
            'rise': sun.get('rise'),
            'set': sun.get('set'),
        }

        for time_element in forecast_xml.xpath('forecast/tabular/time')[:28]:
            weather['forecast'].append({
                'time': time_element.get('from'),
                'description': time_element.find('symbol').get('name'),
                'temperature': time_element.find('temperature').get('value'),
            })

        response = requests.get(
            'https://www.yr.no/place/Sweden/Stockholm/Stockholm/forecast_hour_by_hour.xml',
            headers={
                'user-agent': 'johanli.com',
            },
        )

        forecast_hour_xml = etree.fromstring(response.content)

        for time_element in forecast_hour_xml.xpath('forecast/tabular/time')[:24]:
            weather['forecast_hour'].append({
                'time': time_element.get('from'),
                'description': time_element.find('symbol').get('name'),
                'temperature': time_element.find('temperature').get('value'),
            })

        cache.set('weather', weather, 7200)

    return weather


def forecast():
    weather = get_weather()

    formatted_forecast = OrderedDict()

    for forecast in weather['forecast']:
        datetime_object = datetime.strptime(forecast['time'], '%Y-%m-%dT%H:%M:%S')
        datetime_object_utc = datetime_object + timedelta(hours=1) # yr.no returns local timestamps, not utc

        day = datetime_to_day(datetime_object_utc)

        if day not in formatted_forecast:
            formatted_forecast[day] = []

        formatted_forecast[day].append({
            'description': forecast['description'],
            'temperature': forecast['temperature'],
            'hour': datetime_object.strftime('%H:%M'),
            'icon': get_icon(forecast, weather['sun']),
        })

    return shorten_forecast_after_tomorrow(formatted_forecast)


def datetime_to_day(datetime_object):
    if datetime.utcnow().date() == datetime_object.date():
        return 'Today'
    elif datetime.utcnow().date() + timedelta(days=1) == datetime_object.date():
        return 'Tomorrow'
    else:
        return datetime_object.strftime('%A')


def get_icon(forecast, sun):
    icon = forecast['description'].replace(' ', '-').lower()

    if not icon_has_day_night(icon):
        return icon

    if sun['rise'] <= forecast['time'] < sun['set']:
        return 'day/' + icon
    else:
        return 'night/' + icon


def icon_has_day_night(name):
    return name not in [
        'cloudy',
        'fog',
        'heavy-rain-and-thunder',
        'heavy-rain',
        'heavy-sleet-and-thunder',
        'heavy-sleet',
        'heavy-snow-and-thunder',
        'heavy-snow',
        'light-rain-and-thunder',
        'light-rain',
        'light-sleet-and-thunder',
        'light-sleet',
        'light-snow-and-thunder',
        'light-snow',
        'rain-and-thunder',
        'rain',
        'sleet-and-thunder',
        'sleet',
        'snow-and-thunder',
        'snow',
    ]


def shorten_forecast_after_tomorrow(formatted_forecast):
    for day, forecast in formatted_forecast.items():
        if day in ['Today', 'Tomorrow']:
            continue

        if len(forecast) < 4:
            del formatted_forecast[day]
            continue

        formatted_forecast[day] = [forecast[2]]

    return formatted_forecast
