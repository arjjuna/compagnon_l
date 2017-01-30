from flask import abort, flash, url_for, render_template, redirect, request
from . import admin
from ..decorators import admin_required
from flask_login import login_required
from .forms import ProfForm, UserForm

from .. import db
from ..models import Prof, Client

@admin.route('/')
@login_required
@admin_required
def index():
	return render_template('admin/base.html')
	
@admin.route('/profs')
@login_required
@admin_required
def profs():
	profs = Prof.query.all()
	return render_template('admin/profs.html', profs=profs)	
	
@admin.route('/clients')
@login_required
@admin_required
def clients():
	clients = Client.query.all()
	return render_template('admin/clients.html', clients=clients)
	
@admin.route('/prof<int:prof_id>')
@login_required
@admin_required
def prof(prof_id):
	prof = Prof.query.filter_by(id=prof_id).first()
	return render_template('admin/prof.html', prof=prof)	
	
@admin.route('/edit/prof/prof<int:prof_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_prof(prof_id):
	form = ProfForm()
	prof = Prof.query.filter_by(id=prof_id).first()
	if form.validate_on_submit():
		prof.title = form.title.data
		prof.rate = form.rate.data
		
		db.session.add(prof)
		db.session.commit()
		
		flash('Change made to Prof')
		return redirect(url_for('admin.prof', prof_id=prof.id))
	else:
		form.title.data = prof.title
		form.rate.data = prof.rate 
	
	return render_template('admin/edit_prof.html', prof=prof, form=form)
	
@admin.route('/edit/user/prof<int:prof_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(prof_id):
	form = UserForm()
	prof = Prof.query.filter_by(id=prof_id).first()
	user = prof.user
	if form.validate_on_submit():
		user.first_name = form.first_name.data
		user.last_name = form.last_name.data

		db.session.add(user)
		db.session.commit()
		
		flash('Change made to User')
		return redirect(url_for('admin.prof', prof_id=prof.id))
	else:
		form.first_name.data = user.first_name
		form.last_name.data = user.last_name
	
	return render_template('admin/edit_user.html', prof=prof, form=form)