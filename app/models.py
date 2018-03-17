from . import db

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primany_key=True)
	name = db.Column(db.String, nullable=True)
	users = db.relationship('User', bachref='roles')

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primany_key=True)
	name = db.Column(db.String, nullable=True)
	password = db.Column(db.String, nullable=True)
	role_id = db.Column(db.Integer, db.Foreignkey('roles.id'))