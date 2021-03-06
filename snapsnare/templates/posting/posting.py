import os
import os.path
from uuid import uuid4
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import current_app
from flask import session
from flask import redirect
from flask import url_for
from flask_login import login_required

from snapsnare.system import dictionaries
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system import storage

posting = Blueprint('posting', __name__, template_folder='templates')


@posting.route('/posting', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    user_repository = UserRepository(connector)
    section_repository = SectionRepository(connector)
    role_repository = RoleRepository(connector)

    user = user_repository.find_by_uuid(session['uuid'])

    if request.method == 'GET':
        # retrieve the uuid.
        section_uuid = request.args.get('section')
        uuid_ = request.args.get('uuid')

        sections = section_repository.list()

        if uuid_:
            # contains the uuid of the section

            activity_repository = ActivityRepository(connector)
            activity = activity_repository.find_by_uuid(uuid_)

            posting_ = {
                'section': section_uuid,
                'uuid': uuid_,
                'user': user['uuid'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'content': activity['content'],
                'rendering': activity['rendering']
            }
            connector.close()
            return render_template('posting/posting.html', sections=sections, posting=posting_)

        # contains the uuid of the section
        section_uuid = request.args.get('section')

        user = user_repository.find_by_uuid(session['uuid'])
        section = section_repository.find_by_uuid(section_uuid)
        role = role_repository.find_by_id(section['rle_id'])

        # check messing with the posting in relation to the section
        if session['role'] != role['role']:
            return redirect(url_for('login.show'))

        posting_ = {
            'section': section_uuid,
            'user': user['uuid'],
            'first_name': user['first_name'],
            'last_name': user['last_name']
        }

        connector.close()
        return render_template('posting/posting.html', sections=sections, posting=posting_)

    uuid_ = request.form['uuid']
    user_uuid = request.form['user']
    section_uuid = request.form['section']
    content = request.form['content']
    rendering = request.form.get('rendering')

    # image_as_background = request.form['image_as_background']
    # print('image_as_background', image_as_background)

    # store the uploaded files if given.
    files = request.files

    properties = current_app.properties

    # # create the upload folder for this posting, if not present
    # upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uuid_)
    # if not os.path.isdir(upload_folder):
    #     os.mkdir(upload_folder)
    #
    # for file in files.getlist('file'):
    #     # implicit way to determine if there were files requested for upload
    #     if file.filename:
    #         filename, extension = os.path.splitext(file.filename)
    #         file.save(os.path.join(upload_folder, "{}{}".format(str(uuid4()), extension)))

    activity_repository = ActivityRepository(connector)
    section = section_repository.find_by_uuid(section_uuid)

    if uuid_:
        # persist the uploaded files if any.
        storage.persist_files(properties, uuid_, files)

        activity = {
            'uuid': uuid_,
            'content': content,
            'rendering': rendering
        }

        activity_repository.update(activity)
        connector.commit()
        connector.close()

        # file = request.files['file']
        # print(file)

        flash('Je bericht is bijgewerkt', 'info')
        return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))

    user = user_repository.find_by_uuid(user_uuid)

    # check messing with the posting in relation to the section

    role = role_repository.find_by_id(section['rle_id'])

    if session['role'] != role['role']:
        return redirect(url_for('login.show'))

    # generate a uuid, reflecting functional key of the activity
    uuid_ = str(uuid4())

    # persist the uploaded files if any.
    storage.persist_files(properties, uuid_, files)

    activity = {
        'uuid': uuid_,
        'usr_id': user['id'],
        'stn_id': section['id'],
        'content': content,
        'rendering': rendering
    }
    activity_repository.insert(activity)

    connector.commit()
    connector.close()
    flash('Je bericht is geplaatst', 'info')
    return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))
