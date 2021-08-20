from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_required


from snapsnare.system import dictionaries
from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository

registration = Blueprint('registration', __name__, template_folder='templates')


@registration.route('/registration', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    registration_repository = RegistrationRepository(connector)
    role_repository = RoleRepository(connector)

    role = session.get('role', 'user')
    if role != 'admin':
        return redirect(url_for('login.show'))

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')
        registration_ = registration_repository.find_by_uuid(uuid_)
        registration_ = dictionaries.strip_none(registration_)

        role = role_repository.find_by(id=registration_['rle_id'], active=1)
        registration_['role'] = role['role']

        roles = role_repository.list_by(active=1)

        section_repository = SectionRepository(connector)
        sections = section_repository.list()

        connector.close()
        return render_template('registration/registration.html', sections=sections, registration=registration_, roles=roles)

    uuid_ = request.form['uuid']
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    nickname = request.form['nickname']
    phone_number = request.form['phone_number']
    role = request.form['role']

    role = role_repository.find_by(role=role, active=1)

    registration_ = {
        'uuid': uuid_,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'nickname': nickname,
        'phone_number': phone_number,
        'rle_id': role['id']
    }
    registration_repository.update(registration_)

    registration_ = registration_repository.find_by_uuid(uuid_)
    user_repository = UserRepository(connector)
    user = user_repository.find_by_rgn_id(registration_['id'])

    if user:

        user = {
            'uuid': user['uuid'],
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
            'phone_number': phone_number,
            'rle_id': role['id']
        }

        user_repository.update(user)

    connector.commit()
    connector.close()
    flash('De registratiegegevens zijn bijgewerkt', 'info')
    return redirect(url_for('registrations.show'))
