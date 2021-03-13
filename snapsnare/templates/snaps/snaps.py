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
snaps = Blueprint('snaps', __name__, template_folder='templates')


@snaps.route('/snaps')
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
            section = section_repository.find_by_name('Home')

        snaps_ = snap_repository.list()

        properties = current_app.properties

        for snap in snaps_:
            user = user_repository.find_by_id(snap['usr_id'])
            role = role_repository.find_by_id(user['rle_id'])

            snap['username'] = user.get('username')
            snap['first_name'] = user.get('first_name')
            snap['last_name'] = user.get('last_name')
            snap['role'] = role.get('role')
            snap['section'] = section['uuid']

            dt_created_at = datetime.strptime(snap['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            snap['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')

            clips_folder = os.path.join(properties['current.dir'], 'assets', snap['uuid'])
            if os.path.isdir(clips_folder):
                files = Folder(clips_folder).listdir(filters='.wav;.mp3;.ogg')
                if len(files) != 0:
                    snap['url'] = '/assets/{}/{}'.format(snap['uuid'], files[0])
                    snap['type'] = utils.html_audio_source_type(files[0])

        # retrieve the expected role for this section
        role = role_repository.find_by_id(section['rle_id'])
        section['role'] = role['role']

        # retrieve the sections to show in the navbar
        sections = section_repository.list()

        about = section_repository.find_by_name('Over ons')
        team = section_repository.find_by_name('Team')

        code = {
            'name': snapsnare.__name__,
            'version': snapsnare.__version__,
            'about': about['uuid'],
            'team': team['uuid']
        }

        connector.close()
        return render_template('snaps/snaps.html', sections=sections, code=code, snaps=snaps_, section=section)
