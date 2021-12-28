from flask import Blueprint
from flask import request
from flask import flash
from flask import render_template
from flask import current_app

from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.templates.components import code

activate = Blueprint('activate', __name__, template_folder='templates')


@activate.route('/activate', methods=['GET'])
def show():
    if request.method == 'GET':
        uuid_ = request.args.get('uuid')

        connector = current_app.connector

        registration_repository = RegistrationRepository(connector)
        user_repository = UserRepository(connector)
        role_repository = RoleRepository(connector)

        registration = registration_repository.find_by(uuid=uuid_, active=1, state='new')
        if not registration:
            connector.close()
            flash('Deze gebruiker is al geactiveerd', 'danger')
            return render_template('activate/activate.html', code=code.load())

        role = role_repository.find_by(id=registration['rle_id'], active=1)
        user = {
            'username': registration['username'],
            'password': registration['password'],
            'first_name': registration['first_name'],
            'last_name': registration['last_name'],
            'nickname': registration['nickname'],
            'phone_number': registration['phone_number'],
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
        flash('Gebruiker geactiveerd', 'success')
        return render_template('activate/activate.html', code=code.load())
