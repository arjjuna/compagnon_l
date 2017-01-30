from . import main
from flask import render_template, session, redirect, url_for, flash, send_from_directory, current_app, abort, request

from flask_login import login_required

@main.route('/')
def index():
	return render_template('main/index.html')
	
#A view that "gives urls" to uploaded files in PROJECT_UPLOAD_FOLDER
@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['APP_UPLOAD_FOLDER'], filename)
	
