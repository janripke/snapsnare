from flask import session
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_user

from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system import dictionaries
from snapsnare.templates.login.user import User
from snapsnare.system import hasher


password_forgotten = Blueprint('password_forgotten', __name__, template_folder='templates')


@password_forgotten.route('/password_forgotten', methods=['POST', 'GET'])
def show():
    connector = current_app.connector

    if request.method == 'GET':
        section_repository = SectionRepository(connector)
        sections = section_repository.list_by(active=1, order_by='id')
        connector.close()
        return render_template('password_forgotten/password_forgotten.html', sections=sections)

    username = request.form['username']

    user_repository = UserRepository(connector)
    user = user_repository.find_by_username(username)

    if not user:
        flash('This username is not registered', 'danger')
        return redirect(url_for('register.show'))

    return redirect(request.args.get('next') or url_for('login.show'))