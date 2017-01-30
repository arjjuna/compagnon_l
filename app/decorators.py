from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator
	
def admin_required(f):
	return permission_required(Permission.ADMINISTER)(f)
	
def prof_required(f):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if current_user.prof is None:
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator(f)
		
def client_required(f):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if current_user.client is None:
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator(f)
	