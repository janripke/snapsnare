from datetime import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required

from snapsnare.repositories.registration.registration_repository import RegistrationRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.role.role_repository import RoleRepository
registrations = Blueprint('registrations', __name__, template_folder='templates')


@registrations.route('/registrations', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        connector = current_app.connector
        registration_repository = RegistrationRepository(connector)
        registrations_ = registration_repository.list()

        section_repository = SectionRepository(connector)
        sections = section_repository.list()
        role_repository = RoleRepository(connector)

        for registration in registrations_:
            role = role_repository.find_by_id(registration['rle_id'])

            dt_created_at = datetime.strptime(registration['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            registration['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')
            registration['role'] = role['role']

        connector.close()

        return render_template('registrations/registrations.html', sections=sections, registrations=registrations_)
