import os.path
from uuid import uuid4
from snapsnare.system.folderlib import Folder
from pydub import AudioSegment


def persist_files(properties, uuid_, files):
    # create the assets folder for this posting, if not present
    assets_folder = os.path.join(properties['current.dir'], 'assets', uuid_)

    if not os.path.isdir(assets_folder):
        os.mkdir(assets_folder)

    for file in files.getlist('file'):
        # implicit way to determine if there were files requested for upload
        if file.filename:
            filename, extension = os.path.splitext(file.filename)
            file.save(os.path.join(assets_folder, "{}{}".format(str(uuid4()), extension)))


def convert_m4a_files(properties, uuid_):
    assets_folder = os.path.join(properties['current.dir'], 'assets', uuid_)
    files = Folder(assets_folder).listdir(filters='.m4a')
    for file in files:
        source = os.path.join(assets_folder, file)
        source_path, extension = os.path.splitext(source)
        target = "{}.{}".format(source_path, 'wav')
        if not os.path.isfile(target):
            track = AudioSegment.from_file(source, 'm4a')
            track.export(target, format='wav')
