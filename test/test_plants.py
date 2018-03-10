import unittest
from freezegun import freeze_time
from datetime import datetime
from time import mktime
from libs.plants import needs_watering


@freeze_time("2018-03-10 15:17:34")
class TestWeather(unittest.TestCase):
    def test_needs_watering(self):
        self.assertEqual(
            needs_watering({
                'watering_frequency': 4,
                'last_watered': mktime(datetime(2018, 3, 7, 9, 37, 10).timetuple())
            })['needs_watering'],
            False
        )

        self.assertEqual(
            needs_watering({
                'watering_frequency': 8,
                'last_watered': mktime(datetime(2018, 3, 1, 8, 55, 1).timetuple())
            })['needs_watering'],
            True
        )

    def test_needs_watering_margin(self):
        self.assertEqual(
            needs_watering({
                'watering_frequency': 3,
                'last_watered': mktime(datetime(2018, 3, 7, 17, 17, 35).timetuple())
            })['needs_watering'],
            False
        )

        self.assertEqual(
            needs_watering({
                'watering_frequency': 3,
                'last_watered': mktime(datetime(2018, 3, 7, 17, 17, 34).timetuple())
            })['needs_watering'],
            True
        )
