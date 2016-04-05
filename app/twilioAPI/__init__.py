from flask import Blueprint

twilioAPI = Blueprint('twilioAPI', __name__)

from . import twilioAPI