from flask import Blueprint

bp = Blueprint('nodes', __name__)

from . import views

