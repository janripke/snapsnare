from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required

from snapsnare.repositories.instrument.instrument_repository import InstrumentRepository
from snapsnare.repositories.section.section_repository import SectionRepository
instruments = Blueprint('instruments', __name__, template_folder='templates')


@instruments.route('/instruments', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        connector = current_app.connector
        instrument_repository = InstrumentRepository(connector)
        section_repository = SectionRepository(connector)
        instruments_ = instrument_repository.list_by(active=1, order_by='name')
        sections = section_repository.list()
        connector.close()

        return render_template('instruments/instruments.html', sections=sections, instruments=instruments_)
