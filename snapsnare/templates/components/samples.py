import os
from datetime import datetime
from flask import current_app, request
from snapsnare.repositories.snap.snap_repository import SnapRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system import utils
from snapsnare.system.folderlib import Folder


def load():
    connector = current_app.connector
    section_repository = SectionRepository(connector)
    snap_repository = SnapRepository(connector)
    user_repository = UserRepository(connector)
    role_repository = RoleRepository(connector)

    # retrieve the uuid of the section
    uuid_ = request.args.get('section')
    section = section_repository.find_by_uuid(uuid_)
    if not section:
        # no uuid_ is given, so Home is assumed
        section = section_repository.find_by_name('Home')

    snaps = snap_repository.list_by(active=1, access='public', order_by='updated_at desc')

    properties = current_app.properties

    for snap in snaps:
        user = user_repository.find_by_id(snap['usr_id'])
        role = role_repository.find_by_id(user['rle_id'])

        snap['username'] = user.get('username')
        snap['first_name'] = user.get('first_name')
        snap['last_name'] = user.get('last_name')
        snap['role'] = role.get('role')
        snap['section'] = section['uuid']

        dt_created_at = datetime.strptime(snap['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        snap['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')

        dt_updated_at = datetime.strptime(snap['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
        snap['updated_at_formatted'] = dt_updated_at.strftime('%d %B om %H:%M')

        clips_folder = os.path.join(properties['current.dir'], 'assets', snap['uuid'])
        if os.path.isdir(clips_folder):
            files = Folder(clips_folder).listdir(filters='.wav;.mp3;.ogg')
            if len(files) != 0:
                snap['url'] = '/assets/{}/{}'.format(snap['uuid'], files[0])
                snap['type'] = utils.html_audio_source_type(files[0])

    return snaps
