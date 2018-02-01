import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)


def get(key):
    value = r.get(key)

    if isJson(value):
        return json.loads(value)

    return value


def set(key, value, duration):
    if isList(value):
        value = json.dumps(value)

    if duration:
        return r.set(key, value, ex=duration)
    else:
        return r.set(key, value)


def isJson(value):
    try:
        json.loads(value)
    except Exception:
        return False
    return True


def isList(value):
    return type(value) is list
