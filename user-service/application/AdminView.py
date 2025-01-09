from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from passlib.hash import sha256_crypt

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_app.login'))

class UserAdmin(AdminModelView):
    column_list = ('id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'date_added', 'date_updated')
    form_columns = ('username', 'email', 'first_name', 'last_name', 'password', 'is_admin', 'role_groups')

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = sha256_crypt.hash(str(form.password.data))
        return super(UserAdmin, self).on_model_change(form, model, is_created)
    
    
class RoleGrpAdmin(AdminModelView):
    column_list = ('id', 'name', 'description')
    form_columns = ('name', 'description')
    

class PermissionAdmin(AdminModelView):
    column_list = ('id', 'name', 'description')
    form_columns = ('name', 'description')
    