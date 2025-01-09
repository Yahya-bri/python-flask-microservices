# application/__init__.py
import os
from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from dotenv import load_dotenv
from .AdminView import UserAdmin, RoleGrpAdmin, PermissionAdmin
from .models import User, RoleGroup, Permission, db

# Load environment variables from .env file
load_dotenv()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    admin = Admin(app, name='Admin Users Panel', template_mode='bootstrap4')
    # Register the models with Flask-Admin
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleGrpAdmin(RoleGroup, db.session))
    admin.add_view(PermissionAdmin(Permission, db.session))

    with app.app_context():
        # Create the database if it does not exist
        try:
            # Try to send a request to the database
            db.session.execute('SELECT 1')
        except Exception as e:
            # If it fails, create the database
            db.create_all()

        # Register blueprints
        from .mainApp import user_app_blueprint
        app.register_blueprint(user_app_blueprint, url_prefix='/user')
        from .user_api import user_api_blueprint
        app.register_blueprint(user_api_blueprint, url_prefix='/user_api')

        # Check if a super user exists, if not, create one
        super_user = User.query.filter_by(username='SUPER USER').first()
        if not super_user:
            super_user = User(
                username='SUPER USER',
                email='superuser@example.com',
                password='admin',
                is_admin=True
            )
            super_user.encode_password()
            db.session.add(super_user)
            db.session.commit()

    return app
