import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)


def get(key):
    value = r.get(key)

    if is_json(value):
        return json.loads(value)

    return value


def set(key, value, duration):
    if is_list_or_dict(value):
        value = json.dumps(value)

    if duration:
        return r.set(key, value, ex=duration)
    else:
        return r.set(key, value)


def is_json(value):
    try:
        json.loads(value)
    except Exception:
        return False
    return True


def is_list_or_dict(value):
    return type(value) in [list, dict]
