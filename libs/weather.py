import requests
from lxml import etree
from libs import cache


def get_weather(bust_cache=False):
    if bust_cache:
        weather = []
    else:
        weather = cache.get('weather') or []

    if not weather:
        response = requests.get(
            'https://www.yr.no/place/Sweden/Stockholm/Stockholm/forecast_hour_by_hour.xml',
            headers={
                'user-agent': 'johanli.com',
            },
        )

        weather_xml = etree.fromstring(response.content)

        for time_element in weather_xml.xpath('forecast/tabular/time')[:24]:
            weather.append({
                'time': time_element.get('from'),
                'description': time_element.find('symbol').get('name'),
                'temperature': time_element.find('temperature').get('value'),
            })

        cache.set('weather', weather, 7200)

    return weather
