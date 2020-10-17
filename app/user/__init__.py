from flask import Blueprint, send_from_directory, current_app, jsonify


user = Blueprint('user', __name__)

import app.user.login
import app.user.fileupload