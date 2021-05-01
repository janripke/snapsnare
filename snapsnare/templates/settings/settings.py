from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.templates.components import code

settings = Blueprint('settings', __name__, template_folder='templates')


@settings.route('/settings', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':
        connector = current_app.connector
        section_repository = SectionRepository(connector)
        sections = section_repository.list()

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        return render_template('settings/settings.html', sections=sections, code=code.load())
