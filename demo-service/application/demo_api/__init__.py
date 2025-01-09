# application/order_api/__init__.py
from flask import Blueprint

demo_api_blueprint = Blueprint('demo_api', __name__)

from . import routes