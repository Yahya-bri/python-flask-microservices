# application/user_api/routes.py
from . import user_app_blueprint
from .. import db, login_manager
from ..models import User
from flask import redirect, url_for
from flask_login import logout_user, login_required
from flask import request, flash, render_template
from flask_login import login_user
from .forms import LoginForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@user_app_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@user_app_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
