from flask import render_template, flash, redirect, url_for, abort
from . import prof
from .. import db
from ..decorators import prof_required
from flask_login import login_required, current_user
from ..models import Booking, Prof

@prof.route('/')
@login_required
@prof_required
def index():
	return "Prof side"
	
@prof.route('/bookings')
@login_required
@prof_required
def bookings():
	prof = current_user.prof
	bookings = Booking.query.filter_by(prof=prof)
	return render_template('prof/bookings.html', prof=prof, bookings=bookings)

@prof.route('/booking<int:booking_id>/accept')
@login_required
@prof_required
def accept(booking_id):
	prof = current_user.prof
	booking = Booking.query.filter_by(id=booking_id).first()
	if (booking == None) | (prof != booking.prof) | (booking.accepted == True):
		abort(404)
	else:
		booking.accepted = True
		db.session.add(booking)
		db.session.commit()
		flash('Booking accepted')
		return redirect(url_for('prof.bookings'))