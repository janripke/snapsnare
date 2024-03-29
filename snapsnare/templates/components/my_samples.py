import os
from datetime import datetime
from flask import current_app, session
from snapsnare.repositories.snap.snap_repository import SnapRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.system import utils
from snapsnare.system.folderlib import Folder
from snapsnare.system import component
from snapsnare.system.component import ComponentEnum


def load():
    connector = current_app.connector

    snap_repository = SnapRepository(connector)
    user_repository = UserRepository(connector)
    role_repository = RoleRepository(connector)

    section = component.section()
    if not component.has_fragment(section, ComponentEnum.MY_SAMPLES):
        return []

    user = user_repository.find_by_uuid(session['uuid'])
    snaps = snap_repository.list_by(usr_id=user['id'], active=1, order_by='updated_at desc')

    properties = current_app.properties

    for snap in snaps:
        user = user_repository.find_by(id=snap['usr_id'], active=1)
        role = role_repository.find_by(id=user['rle_id'], active=1)

        snap['username'] = user.get('username')
        snap['first_name'] = user.get('first_name')
        snap['last_name'] = user.get('last_name')
        snap['role'] = role.get('role')
        snap['section'] = section['uuid']

        dt_created_at = datetime.strptime(snap['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        snap['created_at_formatted'] = dt_created_at.strftime('%d %B at %H:%M')

        dt_updated_at = datetime.strptime(snap['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
        snap['updated_at_formatted'] = dt_updated_at.strftime('%d %B at %H:%M')

        clips_folder = os.path.join(properties['current.dir'], 'assets', snap['uuid'])
        if os.path.isdir(clips_folder):
            files = Folder(clips_folder).listdir(filters='.wav;.mp3;.ogg')
            if len(files) != 0:
                snap['url'] = '/assets/{}/{}'.format(snap['uuid'], files[0])
                snap['type'] = utils.html_audio_source_type(files[0])

    return snaps
