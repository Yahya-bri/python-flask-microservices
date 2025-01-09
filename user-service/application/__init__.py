# application/__init__.py
import os
from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from .AdminView import UserAdmin, RoleGrpAdmin, PermissionAdmin
from .models import User, RoleGroup, Permission, db


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')
    # Register the models with Flask-Admin
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleGrpAdmin(RoleGroup, db.session))
    admin.add_view(PermissionAdmin(Permission, db.session))

    with app.app_context():
        # Register blueprints
        from .mainApp import user_app_blueprint
        app.register_blueprint(user_app_blueprint, url_prefix='/user')
        from .user_api import user_api_blueprint
        app.register_blueprint(user_api_blueprint, url_prefix='/user_api')
        return app
