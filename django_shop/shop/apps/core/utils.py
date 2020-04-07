from django.utils.text import slugify
from hashlib import md5

def my_slugify(string):
    return slugify(string, allow_unicode=True)[:64]


def make_hash(string):
    hash = md5(string.encoding())
    return hash.hexdigest()

def get_or_none(model, query):
    try:
        instance = model.objects.get(**query)
    except model.DoesNotExist:
        instance = None
    return instance
