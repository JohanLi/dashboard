from time import time
from libs import cache

default_plants = [
    {
        'name': 'Areca palm',
        'watering_frequency': 3,
    },
    {
        'name': 'Ficus microcarpa',
        'watering_frequency': 3,
    },
    {
        'name': 'Dracaena Marginata',
        'watering_frequency': 7,
    },
    {
        'name': 'White Orchid',
        'watering_frequency': 7,
    },
    {
        'name': 'Clusia',
        'watering_frequency': 7,
    },
]


def get_plants():
    plants = cache.get('plants')

    if not plants:
        plants = default_plants
        cache.set('plants', plants)

    return [needs_watering(plant) for plant in plants]


def needs_watering(plant):
    unix_now = time()
    unix_needs_watering = 86400 * plant['watering_frequency'] + plant.get('last_watered', 0)
    margin = 7200

    if unix_now + margin >= unix_needs_watering:
        plant['needs_watering'] = True
    else:
        plant['needs_watering'] = False

    return plant


def water(id):
    plants = get_plants()
    plants[id]['last_watered'] = time()
    cache.set('plants', plants)
