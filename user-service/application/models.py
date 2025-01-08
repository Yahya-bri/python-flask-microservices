# application/models.py
from . import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from sqlalchemy_serializer import SerializerMixin


class UserRoleGroup(db.Model, SerializerMixin):
    __tablename__ = 'user_role_group'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_group_id = db.Column(db.Integer, db.ForeignKey('role_group.id'), primary_key=True)

class PermissionRoleGroup(db.Model, SerializerMixin):
    __tablename__ = 'permission_role_group'
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)
    role_group_id = db.Column(db.Integer, db.ForeignKey('role_group.id'), primary_key=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    role_groups = db.relationship('RoleGroup', secondary=user_role_group, backref=db.backref('users', lazy=True))

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'api_key': self.api_key,
            'is_active': True,
            'is_admin': self.is_admin
        }


class RoleGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', secondary=user_role_group, backref=db.backref('role_groups', lazy=True))
    permissions = db.relationship('Permission', secondary=permission_role_group, backref=db.backref('role_groups', lazy=True))

    def __repr__(self):
        return '<RoleGroup %r>' % (self.name)

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Permission %r>' % (self.name)

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }