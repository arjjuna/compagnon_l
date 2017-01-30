from flask import Blueprint

testbp = Blueprint('testbp', __name__)

from . import views, errors