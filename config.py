import os
basedir = os.path.abspath(os.path.dirname(__file__))

PROJECT_DB_PASSWORD = os.environ.get('POSTGRES_DB_PASSWORD')	

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'alhsf7a9f623ge97'
	
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
	APP_MAIL_SUBJECT_PREFIX = '[Compagnon]'
	APP_MAIL_SENDER         = 'Compagnon Admin <freelancer.arjjuna@gmail.com>'
	
	APP_ADMIN = os.environ.get('APP_ADMIN') or 'med.tiour@gmail.com' 
	
	
	@staticmethod
	def init_app(app):
		pass
		
class DevelopmentConfig(Config):
	APP_PATH = '/home/arjjuna/flask/projet2/website/app'	
	DEBUG                   = True
	
	APP_UPLOAD_FOLDER =  '/home/arjjuna/flask/projet2/website/app/static/uploads'
	APP_STATIC_FOLDER = '/home/arjjuna/flask/projet2/website/app/static'
	
	MAIL_SERVER             = 'smtp.gmail.com'
	MAIL_PORT               = 587
	MAIL_USE_TLS            = True
	MAIL_USERNAME           = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD           = os.environ.get('MAIL_PASSWORD')
	
	DEV_DATABASE_URL        = 'postgresql://postgres:' + PROJECT_DB_PASSWORD + '@localhost/compagnon'
	SQLALCHEMY_DATABASE_URI = DEV_DATABASE_URL
	
class TestingConfig(Config):
	APP_PATH = '/home/arjjuna/flask/projet2/website/app'
	TESTING                 = True
	
	APP_UPLOAD_FOLDER =  '/home/arjjuna/flask/projet2/website/app/static/testing_uploads'
	APP_STATIC_FOLDER = '/home/arjjuna/flask/projet2/website/app/static'
	
	TEST_DATABASE_URL        = 'postgresql://postgres:' + PROJECT_DB_PASSWORD + '@localhost/compagnon_test'
	SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
	



config = {
	'development': DevelopmentConfig,
	'testing'    : TestingConfig,
	'default'    : DevelopmentConfig
}