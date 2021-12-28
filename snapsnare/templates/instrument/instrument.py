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
from snapsnare.repositories.instrument.instrument_repository import InstrumentRepository
from snapsnare.repositories.section.section_repository import SectionRepository

instrument = Blueprint('instrument', __name__, template_folder='templates')


@instrument.route('/instrument', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    instrument_repository = InstrumentRepository(connector)
    section_repository = SectionRepository(connector)

    sections = section_repository.list_by(active=1, order_by='id')

    role = session.get('role', 'user')
    if role != 'admin':
        return redirect(url_for('login.show'))

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')

        if uuid_:
            instrument_ = instrument_repository.find_by_uuid(uuid_)
            instrument_ = dictionaries.strip_none(instrument_)

            connector.close()
            return render_template('instrument/instrument.html', sections=sections, instrument=instrument_)

        instrument_ = {
        }

        return render_template('instrument/instrument.html', sections=sections, instrument=instrument_)

    if request.method == 'POST':
        uuid_ = request.form['uuid']
        name = request.form['name']

        if uuid_:
            instrument_ = {
                'uuid': uuid_,
                'name': name
            }
            instrument_repository.update(instrument_)

            connector.commit()
            connector.close()
            flash('De instrument details zijn bijgewerkt.', 'info')
            return redirect(url_for('instruments.show'))

        instrument_ = {
            'name': name
        }

        instrument_repository.insert(instrument_)
        connector.commit()
        connector.close()
        flash('Het instrument is toegevoegd.', 'info')
        return redirect(url_for('instruments.show'))
