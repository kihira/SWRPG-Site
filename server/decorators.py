from functools import wraps

from bson import ObjectId
from flask import abort
from pymongo.collection import Collection


def get_item(collection: Collection, objectid=False):
    """
    Decorator that will attempt to get the item from the collection and if its not found, return 404
    :param collection:
    :return:
    """
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if objectid:
                if len(kwargs["item"]) != 24:
                    return abort(404)
                kwargs["item"] = ObjectId(kwargs["item"])

            item = collection.find_one(kwargs["item"])
            if item is None:
                return abort(404)
            kwargs["item"] = item

            return f(*args, **kwargs)
        return wrapper
    return decorated
