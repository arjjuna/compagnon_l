from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..email import send_email
from ..models import User, Prof, Client
from .forms import LoginForm, ProfRegistrationForm, ClientRegistrationForm

@auth.route('/connexion', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index') )
		flash("Nom d'utilisateur ou mot de passe incorrecte")
	return render_template('auth/login.html', form=form)
	
@auth.route('/deconnexion')
@login_required
def logout():
	logout_user()
	flash(u'Vous vous \xeates d\xe9connect\xe9')
	return redirect(url_for('main.index'))
	
@auth.route('/enregistrement_prof', methods=['GET', 'POST'])
def register_prof():
	form = ProfRegistrationForm()
	if form.validate_on_submit():
		prof = Prof(title=form.title.data)
		user = User(email=form.email.data, password=form.password.data,
					first_name=form.first_name.data, last_name=form.last_name.data,
					prof=prof)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirmez votre inscription', 'auth/email/confirm_prof', user=user, token=token)
		flash(u'Un email de confirmation vous a \xeates envoy\xe9')
		return redirect(url_for('auth.login'))
	return render_template('auth/register_prof.html', form=form)	
	
@auth.route('/enregistrement_client', methods=['GET', 'POST'])
def register_client():
	form = ClientRegistrationForm()
	if form.validate_on_submit():
		client = Client(title=form.title.data)
		user = User(email=form.email.data, password=form.password.data,
					first_name=form.first_name.data, last_name=form.last_name.data,
					client=client)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirmez votre inscription', 'auth/email/confirm_client', user=user, token=token)
		flash(u'Un email de confirmation vous a \xeates envoy\xe9')
		return redirect(url_for('auth.login'))
	return render_template('auth/register_client.html', form=form)
	
@auth.route('confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'Confirmation r\xe9ussie')
	else:
		flash(u'Ce lien de confirmation est invalide ou expir\xe9')
	return redirect(url_for('main.index'))
	
@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and (request.endpoint[:5] != 'auth.'):
		return redirect(url_for('auth.unconfirmed'))
		
@auth.route('/non_confirme')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirmez votre inscription', 'auth/email/confirm',  user=current_user, token=token)
	flash(u'Un nouvel email vous a \xe9t\xe9 envoy\xe9.')
	return redirect(url_for('main.index'))
	

		
		