import unittest
from freezegun import freeze_time
from datetime import datetime
from libs.weather import datetime_to_name, get_icon


@freeze_time("2018-02-28 22:35:01")
class TestWeather(unittest.TestCase):
    def test_datetime_to_name_today(self):
        self.assertEqual(datetime_to_name(datetime(2018, 2, 28, 00, 00, 00)), 'Today')
        self.assertEqual(datetime_to_name(datetime(2018, 2, 28, 12, 00, 00)), 'Today')
        self.assertEqual(datetime_to_name(datetime(2018, 2, 28, 23, 59, 59)), 'Today')

    def test_datetime_to_name_tomorrow(self):
        self.assertEqual(datetime_to_name(datetime(2018, 3, 1, 00, 00, 00)), 'Tomorrow')
        self.assertEqual(datetime_to_name(datetime(2018, 3, 1, 12, 00, 00)), 'Tomorrow')
        self.assertEqual(datetime_to_name(datetime(2018, 3, 1, 23, 59, 59)), 'Tomorrow')

    def test_datetime_to_name_days_after(self):
        self.assertEqual(datetime_to_name(datetime(2018, 3, 2, 0, 0, 0)), 'Friday')
        self.assertEqual(datetime_to_name(datetime(2018, 3, 3, 0, 0, 0)), 'Saturday')
        self.assertEqual(datetime_to_name(datetime(2018, 3, 4, 0, 0, 0)), 'Sunday')

    def test_get_icon_day(self):
        self.assertEqual(
            get_icon(
                {
                    'description': 'Clear sky',
                    'time': '2018-03-01T12:00:00'
                },
                {
                    'rise': '2018-03-01T06:45:25',
                    'set': '2018-03-01T17:15:54'
                }
            ),
            'day/clear-sky'
        )
        self.assertEqual(
            get_icon(
                {
                    'description': 'Heavy snow showers',
                    'time': '2020-12-31T10:12:45'
                },
                {
                    'rise': '2020-12-31T10:12:45',
                    'set': '2020-12-31T14:00:00'
                }
            ),
            'day/heavy-snow-showers'
        )

    def test_get_icon_night(self):
        self.assertEqual(
            get_icon(
                {
                    'description': 'Rain showers',
                    'time': '2018-03-01T00:00:00'
                },
                {
                    'rise': '2018-03-01T06:45:25',
                    'set': '2018-03-01T17:15:54'
                }
            ),
            'night/rain-showers'
        )
        self.assertEqual(
            get_icon(
                {
                    'description': 'Light snow showers and thunder',
                    'time': '2020-12-31T14:00:00'
                },
                {
                    'rise': '2020-12-31T10:12:45',
                    'set': '2020-12-31T14:00:00'
                }
            ),
            'night/light-snow-showers-and-thunder'
        )

    def test_get_icon_no_day_night(self):
        self.assertEqual(
            get_icon(
                {
                    'description': 'Light sleet',
                    'time': '2018-03-01T00:00:00'
                },
                {
                    'rise': '2018-03-01T06:45:25',
                    'set': '2018-03-01T17:15:54'
                }
            ),
            'light-sleet'
        )
