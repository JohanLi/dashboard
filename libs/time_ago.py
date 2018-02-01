import time
import math

def time_ago(date):
    seconds = time.time() - date

    days = math.floor(seconds / 86400)

    if days > 0:
        return format(days, 'day')

    hours = math.floor(seconds / 3600)

    if hours > 0:
        return format(hours, 'hour')

    minutes = math.floor(seconds / 60)

    if minutes > 0:
        return format(minutes, 'minute')

    return format(seconds, 'second')


def format(value, unit):
    plural = 's'

    if value == 1:
        plural = ''

    return str(value) + ' ' + unit + plural + ' ago'
