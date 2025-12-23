from functools import wraps
from flask import request, jsonify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # On vérifie si le cookie existe
        token = request.cookies.get('spotify_access_token')

        if not token:
            return jsonify({'error': 'Unauthorized: Please log in'}), 401

        return f(*args, **kwargs)

    return decorated_function