from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import current_app
from flask import flash
from flask_login import login_required

from snapsnare.repositories.snap.snap_repository import SnapRepository
from snapsnare.repositories.file.file_repository import FileRepository
from snapsnare.repositories.section.section_repository import SectionRepository

upload_delete = Blueprint('upload_delete', __name__, template_folder='templates')


@upload_delete.route('/upload/delete', methods=['GET'])
@login_required
def show():
    if request.method == 'GET':

        role = session.get('role', 'user')
        if role != 'admin':
            return redirect(url_for('login.show'))

        uuid_ = request.args.get('uuid')
        section_uuid_ = request.args.get('section')

        connector = current_app.connector
        snap_repository = SnapRepository(connector)
        file_repository = FileRepository(connector)
        section_repository = SectionRepository(connector)
        section = section_repository.find_by_uuid(section_uuid_)

        snap = {
            'uuid': uuid_,
            'active': 0
        }
        snap_repository.update(snap)

        file = {
            'active': 0,
        }
        file_repository.update(file, where={'asset': uuid_})

        connector.commit()
        connector.close()

        flash('Your sample is removed successfully.', 'info')
        return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))
