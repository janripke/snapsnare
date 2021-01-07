from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required

from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
activate = Blueprint('activate', __name__, template_folder='templates')


@activate.route('/activate', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        uuid_ = request.args.get('uuid')

        connector = current_app.connector
        registration_repository = RegistrationRepository(connector)
        user_repository = UserRepository(connector)
        role_repository = RoleRepository(connector)

        registration = registration_repository.find_by_uuid(uuid_)
        role = role_repository.find_by_id(registration['rle_id'])
        user = {
            'username': registration['username'],
            'password': registration['password'],
            'first_name': registration['first_name'],
            'last_name': registration['last_name'],
            'rgn_id': registration['id'],
            'rle_id': role['id']
        }
        user_repository.insert(user)

        registration = {
            'uuid': uuid_,
            'state': 'approved'
        }
        registration_repository.update(registration)
        connector.commit()
        connector.close()

        return redirect(url_for('registrations.show'))
