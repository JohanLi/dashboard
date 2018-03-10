from datetime import datetime, timedelta
from time import mktime


def plants():
    return [needs_watering(plant) for plant in plants_mock()]


def needs_watering(plant):
    unix_now = mktime(datetime.utcnow().timetuple())
    unix_needs_watering = 86400 * plant['watering_frequency'] + plant['last_watered']
    margin = 7200

    if unix_now + margin >= unix_needs_watering:
        plant['needs_watering'] = True
    else:
        plant['needs_watering'] = False

    return plant


def plants_mock():
    return [
        {
            'name': 'Areca palm',
            'watering_frequency': 3,
            'last_watered': mktime((datetime.utcnow() - timedelta(days=1)).timetuple())
        },
        {
            'name': 'Ficus microcarpa',
            'watering_frequency': 3,
            'last_watered': mktime((datetime.utcnow() - timedelta(days=2)).timetuple())
        },
        {
            'name': 'Dracaena Marginata',
            'watering_frequency': 7,
            'last_watered': mktime((datetime.utcnow() - timedelta(days=9)).timetuple())
        },
        {
            'name': 'White Orchid',
            'watering_frequency': 7,
            'last_watered': mktime((datetime.utcnow() - timedelta(days=5)).timetuple())
        },
        {
            'name': 'Clusia',
            'watering_frequency': 7,
            'last_watered': mktime((datetime.utcnow() - timedelta(days=2)).timetuple())
        },
    ]
