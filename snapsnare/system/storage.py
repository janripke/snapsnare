import os.path
from uuid import uuid4
from flask import current_app


def persist_files(uuid_, files):
    # create the upload folder for this posting, if not present
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uuid_)
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)

    for file in files.getlist('file'):
        # implicit way to determine if there were files requested for upload
        if file.filename:
            filename, extension = os.path.splitext(file.filename)
            file.save(os.path.join(upload_folder, "{}{}".format(str(uuid4()), extension)))
