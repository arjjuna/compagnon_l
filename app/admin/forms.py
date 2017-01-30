from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,	DateTimeField, IntegerField, TextField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import DateField

class ProfForm(FlaskForm):
	title = StringField('Titre')
	rate = IntegerField('Prix')
	submit = SubmitField()
	
class UserForm(FlaskForm):
	first_name = StringField('Nom')
	last_name = StringField(u'Pr\xe9nom')
	submit = SubmitField()