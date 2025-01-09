# application/user_api/__init__.py
from flask import Blueprint

user_app_blueprint = Blueprint('user_app', __name__, template_folder='templates')

from . import routes