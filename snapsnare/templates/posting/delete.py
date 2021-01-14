from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask import flash
from flask_login import login_required

from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.user.user_repository import UserRepository

posting_delete = Blueprint('posting_delete', __name__, template_folder='templates')


@posting_delete.route('/posting/delete', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        uuid_ = request.args.get('uuid')
        section_uuid_ = request.args.get('section')

        connector = current_app.connector
        activity_repository = ActivityRepository(connector)
        section_repository = SectionRepository(connector)
        section = section_repository.find_by_uuid(section_uuid_)

        activity = {
            'uuid': uuid_,
            'active': 0
        }
        activity_repository.update(activity)

        connector.commit()
        connector.close()

        flash('Je bericht is verwijderd', 'info')
        return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))
