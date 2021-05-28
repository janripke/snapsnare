import os.path
from uuid import uuid4
from pathlib import Path
from enum import Enum
from snapsnare.system.folderlib import Folder
from pydub import AudioSegment
from flask import current_app, session
from snapsnare.repositories.file.file_repository import FileRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.system import ora


class AssetType(Enum):
    SINGLE = 1
    MULTIPLE = 2


def persist_files(properties, asset, files, asset_type: AssetType = AssetType.SINGLE):
    # create the assets folder for this posting, if not present
    assets_folder = Path() / properties['current.dir'] / 'assets' / asset
    assets_folder.mkdir(parents=True, exist_ok=True)

    for file in files.getlist('file'):
        # implicit way to determine if there were files requested for upload
        if file.filename:
            source = Path(file.filename)
            file_uuid = register_file(asset, file.filename, asset_type=asset_type)
            target = assets_folder / f"{file_uuid}{source.suffix}"
            file.save(target)

            convert_m4a_file(properties, source, asset, target, asset_type)


def register_file(asset, upload_name, override_suffix=None, asset_type: AssetType = AssetType.SINGLE):
    connector = current_app.connector
    file_repository = FileRepository(connector)
    user_repository = UserRepository(connector)
    user = user_repository.find_by_uuid(session['uuid'])

    files = file_repository.list_by(**deactivate_filter(upload_name, asset, asset_type))
    for file in files:
        file['active'] = 0
        file_repository.update(file)

    source = Path(upload_name)
    uuid = uuid4().hex
    file = {
        'uuid': uuid,
        'asset': asset,
        'uploadname': source.name,
        'usr_id': user['id'],
        'filename': ora.nvl2(override_suffix, f"{uuid}{override_suffix}", f"{uuid}{source.suffix}")
    }
    file_repository.insert(file)
    return file['uuid']


def deactivate_filter(uploadname, asset, asset_type: AssetType):
    result = {
        'asset': asset,
        'active': 1,
    }
    if asset_type == AssetType.MULTIPLE:
        result['uploadname'] = uploadname

    return result


def convert_m4a_file(properties, source: Path, asset: str, registration: Path, asset_type: AssetType):
    if source.suffix == '.m4a':
        assets_folder = Path() / properties['current.dir'] / 'assets' / asset
        source = assets_folder / source
        file_uuid = register_file(asset, source.name, override_suffix='.wav', asset_type=asset_type)

        target = assets_folder / f"{file_uuid}.wav"
        track = AudioSegment.from_file(registration, 'm4a')
        track.export(target, format='wav')
