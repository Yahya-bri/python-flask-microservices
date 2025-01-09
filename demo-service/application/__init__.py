# application/__init__.py
import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    db.init_app(app)

    with app.app_context():
        # Create the database if it does not exist
        try:
            # Try to send a request to the database
            db.session.execute('SELECT 1')
        except Exception as e:
            # If it fails, create the database
            db.create_all()

        from .demo_api import demo_api_blueprint
        app.register_blueprint(demo_api_blueprint, url_prefix='/demo_api')
        return app
