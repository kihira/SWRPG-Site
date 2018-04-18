from functools import wraps

from bson import ObjectId
from flask import abort, session, redirect, url_for
from pymongo.collection import Collection
from server import login


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


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Only have admin users for now, this should be fine
        if "username" in session and session["username"] in login.users:
            return f(*args, **kwargs)
        return redirect(url_for("login"))

    return wrapper
