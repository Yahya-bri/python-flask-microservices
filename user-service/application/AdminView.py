from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class UserAdmin(AdminModelView):
    column_list = ('id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'date_added', 'date_updated')
    form_columns = ('username', 'email', 'first_name', 'last_name', 'password', 'is_admin', 'role_groups')
    
    
class RoleGrpAdmin(AdminModelView):
    column_list = ('id', 'name', 'description')
    form_columns = ('name', 'description')
    

class PermissionAdmin(AdminModelView):
    column_list = ('id', 'name', 'description')
    form_columns = ('name', 'description')
    