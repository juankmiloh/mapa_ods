from functools import wraps
from flask import current_app, request, abort 

def privateDecorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.config.get("PUBLIC"):
            return abort(401)

        return f(*args, **kwargs)
    return decorated_function

def isPublic():
    return current_app.config.get("PUBLIC")
