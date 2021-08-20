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

from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.snap.snap_repository import SnapRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.instrument.instrument_repository import InstrumentRepository
from snapsnare.repositories.access_modifier.access_modifier_repository import AccessModifierRepository
from snapsnare.repositories.genre.genre_repository import GenreRepository
from snapsnare.system import storage

upload = Blueprint('upload', __name__, template_folder='templates')


@upload.route('/upload', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    user_repository = UserRepository(connector)
    section_repository = SectionRepository(connector)
    role_repository = RoleRepository(connector)
    instrument_repository = InstrumentRepository(connector)
    access_modifier_repository = AccessModifierRepository(connector)
    genre_repository = GenreRepository(connector)
    user = user_repository.find_by_uuid(session['uuid'])

    if request.method == 'GET':
        # retrieve the uuid.
        section_uuid = request.args.get('section')
        uuid_ = request.args.get('uuid')

        # retrieve the instruments
        instruments = instrument_repository.list_by(active=1, order_by='name')
        access_modifiers = access_modifier_repository.list_by(active=1, order_by='modifier')
        genres = genre_repository.list_by(active=1, order_by='genre')

        sections = section_repository.list()

        if uuid_:
            # contains the uuid of the section

            snap_repository = SnapRepository(connector)
            snap = snap_repository.find_by_uuid(uuid_)

            upload_ = {
                'section': section_uuid,
                'uuid': uuid_,
                'user': user['uuid'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'title': snap['title'],
                'access': snap['access'],
                'instrument': snap['instrument'],
                'genre': snap['genre'],
                'chord_schema': snap['chord_schema']
            }

            connector.close()
            return render_template(
                'upload/upload.html',
                sections=sections,
                upload=upload_,
                instruments=instruments,
                access_modifiers=access_modifiers,
                genres=genres)

        # contains the uuid of the section
        section_uuid = request.args.get('section')

        user = user_repository.find_by_uuid(session['uuid'])
        section = section_repository.find_by_uuid(section_uuid)
        role = role_repository.find_by(id=section['rle_id'], active=1)

        # check messing with the posting in relation to the section
        if session['role'] != role['role']:
            return redirect(url_for('login.show'))

        upload_ = {
            'section': section_uuid,
            'user': user['uuid'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'access': "public"
        }

        connector.close()
        return render_template(
            'upload/upload.html',
            sections=sections,
            upload=upload_,
            instruments=instruments,
            access_modifiers=access_modifiers,
            genres=genres)

    if request.method == 'POST':
        uuid_ = request.form['uuid']
        user_uuid = request.form['user']
        section_uuid = request.form['section']
        title = request.form['title']
        instrument = request.form['instrument']
        access = request.form['access']
        genre = request.form['genre']
        chord_schema = request.form['chord_schema']

        # image_as_background = request.form['image_as_background']
        # print('image_as_background', image_as_background)

        # store the uploaded files if given.
        files = request.files

        properties = current_app.properties

        snap_repository = SnapRepository(connector)
        section = section_repository.find_by_uuid(section_uuid)

        if uuid_:

            # persist the uploaded files if any.
            storage.persist_files(properties, uuid_, files, storage.AssetType.SINGLE)

            snap_ = {
                'uuid': uuid_,
                'title': title,
                'access': access,
                'instrument': instrument,
                'genre': genre,
                'chord_schema': chord_schema
            }

            snap_repository.update(snap_)
            connector.commit()
            connector.close()

            flash('Je sample is bijgewerkt', 'info')
            return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))

        user = user_repository.find_by_uuid(user_uuid)

        # check messing with the posting in relation to the section
        role = role_repository.find_by(id=section['rle_id'], active=1)

        if session['role'] != role['role']:
            return redirect(url_for('login.show'))

        # generate a uuid, reflecting functional key of the activity
        uuid_ = str(uuid4())

        # persist the uploaded files if any.
        storage.persist_files(properties, uuid_, files, storage.AssetType.SINGLE)

        snap_ = {
            'uuid': uuid_,
            'usr_id': user['id'],
            'title': title,
            'access': access,
            'instrument': instrument,
            'genre': genre,
            'chord_schema': chord_schema
        }
        snap_repository.insert(snap_)

        connector.commit()
        connector.close()
        flash('Je sample is geplaatst', 'info')
        return redirect(url_for('{}.show'.format(section['endpoint']), section=section['uuid']))
