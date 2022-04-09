from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask import session
from flask_login import login_required

from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system import dictionaries
from snapsnare.templates.login.user import User
from snapsnare.system import hasher

reset = Blueprint('reset', __name__, template_folder='templates')


@reset.route('/reset', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
