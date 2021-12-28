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
from snapsnare.repositories.template.template_repository import TemplateRepository
from snapsnare.system import hasher, utils, gmail


register = Blueprint('register', __name__, template_folder='templates')


@register.route('/register', methods=['GET', 'POST'])
def show():
    connector = current_app.connector
    if request.method == 'GET':

        properties = current_app.properties

        section_repository = SectionRepository(connector)
        sections = section_repository.list_by(active=1, order_by='id')
        return render_template('register/register.html', sections=sections)

    if request.method == 'POST':

        register_repository = RegistrationRepository(connector)
        role_repository = RoleRepository(connector)
        template_repository = TemplateRepository(connector)

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
            'password': hasher.sha256(password),
            'uuid': str(uuid4()),
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
            'phone_number': phone_number,
            'rle_id': role['id']
        }

        id_ = register_repository.insert(registration)
        print("registration created with id ", id_)

        properties = current_app.properties
        settings = utils.load_json(properties, 'snapsnare.json')
        credentials = settings['gmail']
        snapsnare = settings['snapsnare']
        host = snapsnare['host']

        template = template_repository.find_by(template='activate')
        content = template['content']
        content = content.replace("{host}", host)
        content = content.replace("{uuid}", registration['uuid'])

        connector.commit()
        connector.close()

        gmail.send_email(credentials, registration['username'], "activeer je account bij snapsnare.org", content)

        flash('De registratie is geslaagd, er wordt een activerings e-mail gestuurd.', 'success')
        return redirect(url_for('register.show'))
