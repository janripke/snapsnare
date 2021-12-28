from datetime import datetime
from flask import Blueprint, render_template
from flask import request
from flask import current_app
from flask_login import login_required

import os.path
import os
import snapsnare
from snapsnare.repositories.snap.snap_repository import SnapRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system.folderlib import Folder
from markupsafe import Markup
from snapsnare.system import utils
from snapsnare.system import jamulus

jamulus_ = Blueprint('jamulus', __name__, template_folder='templates')


@jamulus_.route('/jamulus')
@login_required
def show():
    if request.method == 'GET':
        connector = current_app.connector
        snap_repository = SnapRepository(connector)
        user_repository = UserRepository(connector)
        role_repository = RoleRepository(connector)
        section_repository = SectionRepository(connector)

        # retrieve the uuid of the section
        uuid_ = request.args.get('section')
        section = section_repository.find_by_uuid(uuid_)
        if not section:
            # no uuid_ is given, so Home is assumed
            section = section_repository.find_by(name='Home', active=1)

        # retrieve the expected role for this section
        role = role_repository.find_by(id=section['rle_id'], active=1)
        section['role'] = role['role']

        # retrieve the sections to show in the navbar
        sections = section_repository.list_by(active=1, order_by='id')

        status = jamulus.status()

        about = section_repository.find_by(name='Over ons', active=1)
        team = section_repository.find_by(name='Team', active=1)

        code = {
            'name': snapsnare.__name__,
            'version': snapsnare.__version__,
            'about': about['uuid'],
            'team': team['uuid']
        }

        connector.close()
        return render_template('snaps/snaps.html', sections=sections, status=status, code=code, section=section)
