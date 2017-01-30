from flask import abort, flash, url_for, render_template, redirect, request, current_app
from . import client
from .. import db
from ..models import Prof, Client, Booking, Comment
from ..decorators import client_required
from flask_login import login_required, current_user
from .forms import BookingForm, CommentForm, PictureForm, CropForm

from werkzeug import secure_filename
from PIL import Image

#A function that resizes a picture
def crop_resize(img_path, x, y, w, h):
    im = Image.open(img_path)
    background = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    background.paste(im, (-x, -y))
    im.close()
    
    return background

@client.route('/')
@login_required
@client_required
def index():
	user = current_user
	return render_template('client/index.html', user=user)
	
@client.route('/profile')
@login_required
@client_required
def profile():
	user = current_user
	return render_template('client/profile.html', user=user)
	
@client.route('/edit/profile', methods=['GET', 'POST'])
@login_required
@client_required
def edit_profile():
	user = current_user
	picture_form = PictureForm()
	if picture_form.validate_on_submit():
		filename_picture = secure_filename("user" + "_" + str(user.id) + "client" + "_" + str(user.client.id) + "_" + picture_form.picture.data.filename)
		picture_form.picture.data.save( current_app.config['APP_UPLOAD_FOLDER'] + '/' + filename_picture)
		picture_url = url_for('main.uploaded_file', filename=filename_picture)
		
		user.picture  = picture_url
		
		db.session.add(user)
		db.session.commit()
		db.session.rollback()
		
		flash(u"Photo mise \xb7 jour")
		return redirect(url_for('client.edit_image'))
	return render_template('client/edit_profile.html', user=user, picture_form=picture_form)
	
#The page for cropping and resizing the images	
@client.route('/edit/image', methods=['GET', 'POST'])
@login_required
@client_required
def edit_image():
	dimension  = (150, 150)
	user       = current_user
	image      = user.picture


	form = CropForm()
	
	if form.validate_on_submit():		
		cropped  = crop_resize(current_app.config['APP_STATIC_FOLDER'] + image, int(form.x.data), int(form.y.data), int(form.width.data), int(form.height.data))
		cropped.save(current_app.config['APP_STATIC_FOLDER'] +  image)
		
		#Not necesary, unless you come up with a way to rename the picture
		user.picture = image

		
		db.session.commit()		
		flash(u"Image sauvegard\xe9e")
		

		return redirect(url_for('client.edit_profile'))
	
		
	return render_template('client/edit_image.html', user=user, image=image, form=form, dimension=dimension)
	
	
	
@client.route('/profs')
@login_required
@client_required
def profs():
	profs = Prof.query.all()
	client = current_user.client
	return render_template('client/profs.html', profs=profs, client=client)
	
@client.route('/book/prof<int:prof_id>', methods=['GET', 'POST'])
@login_required
@client_required
def book(prof_id):
	form = BookingForm()
	prof = Prof.query.filter_by(id=prof_id).first()
	if prof == None:
		abort(404)
	else:
		client = current_user.client
		if form.validate_on_submit():
			booking = Booking(client=client, prof=prof, time=form.time.data,  start=form.start.data)
			db.session.add(booking)
			db.session.commit()
			flash('booking made')
			return redirect(request.args.get('next') or url_for('main.index') )
	return render_template('client/book.html', form=form, prof=prof)
	
@client.route('/bookings')
@login_required
@client_required
def bookings():
	client = current_user.client
	bookings = Booking.query.filter_by(client=client)
	return render_template('client/bookings.html', bookings=bookings, client=client)
		
@client.route('/booking<int:booking_id>', methods=['GET', 'POST'])
@login_required
@client_required
def booking(booking_id):
	client = current_user.client
	booking = Booking.query.filter_by(id=booking_id).first()
	if (booking == None) | (client != booking.client):
		abort(404)
	else:
		return render_template('client/booking.html', booking=booking, client=client)
	
@client.route('/booking<int:booking_id>/validate')
@login_required
@client_required
def validate(booking_id):
	client = current_user.client
	booking = Booking.query.filter_by(id=booking_id).first()
	if (booking == None) | (client != booking.client) | (booking.done == True):
		abort(404)
	else:
		booking.done = True
		comment = Comment(booking=booking)
		db.session.add(booking)
		db.session.add(comment)
		db.session.commit()
		flash('Booking done')
		return redirect(url_for('client.comment', booking_id = booking.id))
	
@client.route('/booking<int:booking_id>/comment', methods=['GET', 'POST'])
@login_required
@client_required
def comment(booking_id):
	form = CommentForm()
	client = current_user.client
	booking = Booking.query.filter_by(id=booking_id).first()
	comment = booking.comment
	if (booking == None) | (comment == None) | (client != booking.client):
		abort(404)
	if comment.score != None:
		abort(404)
	else:
		if form.validate_on_submit():
			comment.score = form.score.data
			comment.text = form.text.data
			db.session.add(comment)
			db.session.commit()
			return redirect(url_for('client.bookings' ))
		return render_template('client/comment.html', form=form, client=client)
	