from datetime import datetime
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required

from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.role.role_repository import RoleRepository
sections = Blueprint('sections', __name__, template_folder='templates')


@sections.route('/sections', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        connector = current_app.connector
        section_repository = SectionRepository(connector)
        sections_ = section_repository.list_by(active=1, order_by='id')

        role_repository = RoleRepository(connector)

        for section in sections_:
            role = role_repository.find_by(id=section['rle_id'], active=1)

            dt_created_at = datetime.strptime(section['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            section['created_at_formatted'] = dt_created_at.strftime('%d %B at %H:%M')
            section['role'] = role['role']

        connector.close()

        return render_template('sections/sections.html', sections=sections_)
