from datetime import datetime
from flask import Blueprint, render_template
from flask import request
from flask import current_app
import os.path
import os
import json
import snapsnare
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.jammer.jammer_repository import JammerRepository
from snapsnare.repositories.icecast_status.icecast_status_repository import IcecastStatusRepository

from snapsnare.system.folderlib import Folder
from markupsafe import Markup
from snapsnare.system.requestors import RestRequest, BearerRequest
index = Blueprint('index', __name__, template_folder='templates')


@index.route('/')
def show():
    if request.method == 'GET':
        connector = current_app.connector
        activity_repository = ActivityRepository(connector)
        user_repository = UserRepository(connector)
        role_repository = RoleRepository(connector)
        section_repository = SectionRepository(connector)
        jammer_repository = JammerRepository(connector)
        icecast_status_repository = IcecastStatusRepository(connector)

        # retrieve the uuid of the section
        uuid_ = request.args.get('section')
        section = section_repository.find_by_uuid(uuid_)
        if not section:
            # no uuid_ is given, so Home is assumed
            section = section_repository.find_by_name('Home')

        activities = activity_repository.list_by_stn_id(section.get('id', -1))

        properties = current_app.properties

        for activity in activities:
            user = user_repository.find_by_id(activity['usr_id'])
            role = role_repository.find_by_id(user['rle_id'])

            content = activity['content']
            if content:
                content = content.replace('\n', '<br>')

            activity['username'] = user.get('username')
            activity['first_name'] = user.get('first_name')
            activity['last_name'] = user.get('last_name')
            activity['role'] = role.get('role')
            activity['section'] = section['uuid']
            activity['content'] = Markup(content)
            activity['slide_count'] = 0

            dt_created_at = datetime.strptime(activity['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            activity['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')

            # for now we only use .png, .jpg and .gif images
            # slides_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], activity['uuid'])
            slides_folder = os.path.join(properties['current.dir'], 'assets', activity['uuid'])
            slides = []
            if os.path.isdir(slides_folder):
                files = Folder(slides_folder).listdir(filters='.png;.jpg;.gif;.jpeg')
                activity['slide_count'] = len(files)
                index_ = 0
                for file in files:
                    slide = {
                        'url': '/assets/{}/{}'.format(activity['uuid'], file),
                        'index': index_
                    }
                    slides.append(slide)
                    index_ += 1
            activity['slides'] = slides

            # for now we only use .mp4 and .mov
            # clips_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], activity['uuid'])
            clips_folder = os.path.join(properties['current.dir'], 'assets', activity['uuid'])
            clips = []
            if os.path.isdir(clips_folder):
                files = Folder(clips_folder).listdir(filters='.mp4;.MOV')
                activity['clip_count'] = len(files)
                index_ = 0
                for file in files:
                    clip = {
                        'url': '/assets/{}/{}'.format(activity['uuid'], file),
                        'index': index_
                    }
                    clips.append(clip)
                    index_ += 1
            activity['clips'] = clips

        # retrieve the expected role for this section
        role = role_repository.find_by_id(section['rle_id'])
        section['role'] = role['role']

        # retrieve the sections to show in the navbar
        sections = section_repository.list()

        # retrieve the live jammers on the jamulus snapsnare server.
        # live jammers are available in the jammers repository

        jammers = jammer_repository.find_by(order_by='id desc')
        jammers['jammers'] = Markup(jammers.get('jammers'))
        dt_created_at = datetime.strptime(jammers['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        jammers['created_at_formatted'] = dt_created_at.strftime('%d %B om %H:%M')

        if not jammers['jammers']:
            jammers['jammers'] = 'Geen actieve jammers'

        icecast_status = icecast_status_repository.find_by(order_by='id desc')
        if icecast_status:
            icecast_status['source'] = json.loads(icecast_status['source'])

        about = section_repository.find_by_name('Over ons')
        team = section_repository.find_by_name('Team')

        code = {
            'name': snapsnare.__name__,
            'version': snapsnare.__version__,
            'about': about['uuid'],
            'team': team['uuid']
        }

        connector.close()
        return render_template('index/index.html', sections=sections, code=code, activities=activities, section=section, jammers=jammers, icecast_status=icecast_status)
