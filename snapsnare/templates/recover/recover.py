from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask import flash
from flask_login import login_required

from snapsnare.repositories.registration.registration_repository import RegistrationRepository

recover = Blueprint('recover', __name__, template_folder='templates')


@recover.route('/recover', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        uuid_ = request.args.get('uuid')

        connector = current_app.connector
        registration_repository = RegistrationRepository(connector)

        registration = registration_repository.find_by_uuid(uuid_)
        if registration['state'] != 'rejected':
            flash('Onverwachte registratie status', 'danger')
            return redirect(url_for('registrations.show'))

        registration = {
            'uuid': uuid_,
            'state': 'new'
        }
        registration_repository.update(registration)
        connector.commit()
        connector.close()

        return redirect(url_for('registrations.show'))
