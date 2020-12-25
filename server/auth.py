from functools import wraps

from flask import request, Response, abort

from server import reloader


def authenticate():
    return Response(
        'Could not verify your access level for that URL. '
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        config = reloader.get_config()
        if auth is None or auth.password != config['SERVER_PASSWORD']:
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def api_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        config = reloader.get_config()
        if auth != config['SERVER_PASSWORD']:
            abort(403)
        return f(*args, **kwargs)

    return decorated
