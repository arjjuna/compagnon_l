from flask import current_app
from . import db
from . import login_manager

from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Permission:
	EDIT_SELF = 0x01
	EDIT_OTHERS = 0x02
	ADMINISTER  = 0x08
	

class Role(db.Model):
	__tablename__ = 'roles'
	id            = db.Column(db.Integer, primary_key=True)
	name          = db.Column(db.String(64), unique=True)
	default       = db.Column(db.Boolean, default=False, index=True)
	permissions   = db.Column(db.Integer)
		
	users = db.relationship('User', backref='role')
	
	@staticmethod
	def insert_roles():
		roles = {
			'user': (Permission.EDIT_SELF, True),
			'administrator': (Permission.ADMINISTER, False) 
		}
		
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()
			
	
	def __repr__(self):
		return '<Role %r>' % self.last_name
	

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id            = db.Column(db.Integer, primary_key=True)
	email         = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(128))
	first_name    = db.Column(db.String(64))
	last_name     = db.Column(db.String(64))
	picture       = db.Column(db.String(500))
	member_since  = db.Column(db.DateTime(), default=datetime.utcnow)
	confirmed     = db.Column(db.Boolean, default=False)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	
	prof = db.relationship('Prof', backref='user', uselist=False)
	client = db.relationship('Client', backref='user', uselist=False)
	
	def is_prof():
		pass
	
	def is_client():
		pass
	
	@property
	def password(self):
		raise AttributeError("password is not a readable attribute")
		
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
		
	def generate_confirmation_token(self, expiration=24*3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})
	
	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		db.session.commit()
		return True
		
	def can(self, permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions
	
	def is_administrator(self):
		return self.role.name == 'administrator'
	
	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['APP_ADMIN']:
				self.role = Role.query.filter_by(name='administrator').first()
			if self.role is None:
				self.role = Role.query.filter_by(name='user').first()
			if self.picture is None:
				self.picture = current_app.config['APP_UPLOAD_FOLDER'] + '/' + "150x150_placeholder.png"
	
	def __repr__(self):
		return '<User %r, email: %r>' % (self.username, self.email)
		
class AnonymousUser(AnonymousUserMixin):
	def can(self, permission):
		return false
	def is_administrator(self, permission):
		return false
		
login_manager.anonymous_user = AnonymousUser
	
class Prof(UserMixin, db.Model):
	__tablename__ = 'profs'
	id            = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	rate = db.Column(db.Integer)
	credit = db.Column(db.Integer, default=0)
	bookings = db.relationship('Booking', backref='prof')

	
	def __repr__(self):
		return '<Prof>'	
		
class Client(UserMixin, db.Model):
	__tablename__ = 'clients'
	id            = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	bookings = db.relationship('Booking', backref='client')
	credit = db.Column(db.Integer, default=0)
	
	def __repr__(self):
		return '<Client>'
		
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
	
class Booking(db.Model):
	__tablename__ = 'bookings'
	id            = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.DateTime)
	start = db.Column(db.Integer)
	done = db.Column(db.Boolean, default=False)
	commented = db.Column(db.Boolean, default=False)
	accepted = db.Column(db.Boolean, default=False)
	past_due = db.Column(db.Boolean, default=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	
	prof_id = db.Column(db.Integer, db.ForeignKey('profs.id'))
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	
	def __repr__(self):
		return '<Booking>'
		
class Comment(db.Model):
	__tablename__ = 'comments'
	id            = db.Column(db.Integer, primary_key=True)
	score = db.Column(db.Integer)
	text = db.Column(db.String(300))
	booking = db.relationship('Booking', backref='comment', uselist=False)
	
class Subject(db.Model):
	__tablename__ = 'subjects'
	id            = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	
class Level(db.Model):
	__tablename__ = 'levels'
	id            = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	name = db.Column(db.String(50))