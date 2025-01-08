from flask import jsonify, request, make_response
from . import user_api_blueprint
from .. import db
from ..models import User, RoleGroup, Permission
from .api.UserClient import UserClient
from flask import g
from functools import wraps


def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('Authorization')
            response = UserClient.get_user(api_key)

            if not response:
                return make_response(jsonify({'message': 'Not logged in'}), 401)

            user = response['result']
            
            if permission_name not in [permission.name for permission in user.permissions]:
                return make_response(jsonify({'message': 'User does not have the required permissions'}), 403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


