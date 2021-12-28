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
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.templates.login.user import User


login = Blueprint('login', __name__, template_folder='templates')


@login.route('/login', methods=['GET', 'POST'])
def show():
    connector = current_app.connector

    if request.method == 'GET':
        section_repository = SectionRepository(connector)
        sections = section_repository.list_by(active=1, order_by='id')
        connector.close()
        return render_template('login/login.html', sections=sections)

    username = request.form['username']
    password = request.form['password']

    user_repository = UserRepository(connector)
    user = user_repository.find_by_username(username)

    if not user:
        flash('Ongeldige gebruikersnaam of wachtwoord', 'danger')
        return redirect(url_for('login.show'))

    registration_repository = RegistrationRepository(connector)
    registration = registration_repository.find_by(id=user['rgn_id'], active=1)
    if registration['state'] == 'blocked':
        flash('Deze gebruiker is geblokkeerd', 'danger')
        return redirect(url_for('login.show'))

    registered_user = User(user['uuid'], user['username'], user['password'])

    if not registered_user.check_password(password):
        flash('Ongeldige gebruikersnaam of wachtwoord', 'danger')
        return redirect(url_for('login.show'))

    role_repository = RoleRepository(connector)
    role = role_repository.find_by(id=user['rle_id'], active=1)
    connector.close()

    login_user(registered_user)
    session['username'] = request.form['username']
    session['uuid'] = user['uuid']
    session['role'] = role['role']

    return redirect(request.args.get('next') or url_for('index.show'))

