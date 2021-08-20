import uuid

from uuid import uuid4
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app

from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.role.role_repository import RoleRepository

register = Blueprint('register', __name__, template_folder='templates')


@register.route('/register', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    if request.method == 'GET':

        properties = current_app.properties



        section_repository = SectionRepository(connector)
        sections = section_repository.list()
        return render_template('register/register.html', sections=sections)

    if request.method == 'POST':

        register_repository = RegistrationRepository(connector)
        role_repository = RoleRepository(connector)

        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['nickname']
        phone_number = request.form['phone_number']

        registered = register_repository.is_registered(username)
        if registered:
            connector.close()
            flash('Deze gebruiker heeft zich al geregistreerd', 'danger')
            return redirect(url_for('register.show'))

        role = role_repository.find_by(role='user', active=1)

        registration = {
            'username': username,
            'password': password,
            'uuid': str(uuid4()),
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
            'phone_number': phone_number,
            'rle_id': role['id']
        }

        id_ = register_repository.insert(registration)
        print("registration created with id ", id_)
        connector.commit()
        connector.close()

        flash('De registratie is geslaagd, er wordt een activerings e-mail gestuurd wanneer je account is goedgekeurd.', 'success')
        return redirect(url_for('register.show'))
