# application/order_api/routes.py
from flask import jsonify, request, make_response
from . import demo_api_blueprint
from .. import db
from ..models import Library
from .api.UserClient import UserClient
from functools import wraps


def require_api_key_and_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('Authorization')
            if not api_key:
                return make_response(jsonify({'message': 'API key is missing'}), 401)
            
            user = UserClient.get_user(api_key)
            user_data = user.get('result', {})
            if not user:
                return make_response(jsonify({'message': 'Invalid API key'}), 401)
            
            user_permissions = [perm for perm in user_data.get('permissions', [])]
            print(user_permissions)
            if permission_name not in user_permissions:
                return make_response(jsonify({'message': 'Permission denied'}), 403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@demo_api_blueprint.route('/api/libraries', methods=['GET'])
@require_api_key_and_permission('TEST_PERMISSION')
def get_libraries():
    libraries = Library.query.all()
    return jsonify([library.to_json() for library in libraries])


@demo_api_blueprint.route('/api/libraries/<int:id>', methods=['GET'])
@require_api_key_and_permission('TEST_PERMISSION')
def get_library(id):
    library = Library.query.get_or_404(id)
    return jsonify(library.to_json())


@demo_api_blueprint.route('/api/libraries', methods=['POST'])
@require_api_key_and_permission('TEST_PERMISSION')
def create_library():
    data = request.get_json()
    new_library = Library(
        name=data['name'],
        address=data['address']
    )
    db.session.add(new_library)
    db.session.commit()
    return jsonify(new_library.to_json()), 201


@demo_api_blueprint.route('/api/libraries/<int:id>', methods=['PUT'])
@require_api_key_and_permission('TEST_PERMISSION')
def update_library(id):
    data = request.get_json()
    library = Library.query.get_or_404(id)
    library.name = data['name']
    library.address = data['address']
    db.session.commit()
    return jsonify(library.to_json())


@demo_api_blueprint.route('/api/libraries/<int:id>', methods=['DELETE'])
@require_api_key_and_permission('TEST_PERMISSION')
def delete_library(id):
    library = Library.query.get_or_404(id)
    db.session.delete(library)
    db.session.commit()
    return jsonify({'message': 'Library deleted successfully'})