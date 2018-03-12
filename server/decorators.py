from functools import wraps

from flask import flash, redirect, url_for


def validate_objectid(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if len(kwargs["object_id"]) != 24:
            # flash("Invalid object id")
            return redirect(url_for('404'))  # todo
        return func(*args, **kwargs)

    return decorated_function
