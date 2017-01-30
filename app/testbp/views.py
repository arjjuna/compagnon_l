from . import testbp
from flask import render_template, session, redirect, url_for, flash, send_from_directory, current_app, abort, request

from flask_login import login_required

from flask_socketio import SocketIO, send

@testbp.route('/')
def index():
	return "Index of the test bp"
	

	
