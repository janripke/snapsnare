from datetime import datetime
from flask import Blueprint, render_template
from flask import request
from flask import current_app
import os.path
import os
import snapsnare
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system.folderlib import Folder
from markupsafe import Markup
index = Blueprint('index', __name__, template_folder='templates')


@index.route('/')
def show():
    if request.method == 'GET':
        connector = current_app.connector
        activity_repository = ActivityRepository(connector)
        user_repository = UserRepository(connector)
        role_repository = RoleRepository(connector)
        section_repository = SectionRepository(connector)

        # retrieve the uuid of the section
        uuid_ = request.args.get('section')
        section = section_repository.find_by_uuid(uuid_)
        if not section:
            # no uuid_ is given, so Home is assumed
            section = section_repository.find_by_name('Home')

        activities = activity_repository.list_by_stn_id(section.get('id', -1))

        properties = current_app.properties
        package_folder = properties['package.dir']

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
            slides_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], activity['uuid'])
            slides = []
            if os.path.isdir(slides_folder):
                files = Folder(slides_folder).listdir(filters='.png;.jpg;.gif')
                activity['slide_count'] = len(files)
                index_ = 0
                for file in files:
                    slide = {
                        'url': '/static/{}/{}'.format(activity['uuid'], file),
                        'index': index_
                    }
                    slides.append(slide)
                    index_ += 1
            activity['slides'] = slides

            # for now we only use .mp4
            clips_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], activity['uuid'])
            clips = []
            if os.path.isdir(clips_folder):
                files = Folder(clips_folder).listdir(filters='.mp4')
                activity['clip_count'] = len(files)
                index_ = 0
                for file in files:
                    clip = {
                        'url': '/static/{}/{}'.format(activity['uuid'], file),
                        'index': index_
                    }
                    clips.append(clip)
                    index_ += 1
            activity['clips'] = clips



        # # retrieve the files contained in the carousel folder
        # carousel_folder = os.path.join(package_folder, 'static', 'd1cc7584-eb2e-4394-8ac0-28906bc844d2')
        # slides = []
        # index_ = 0
        # if os.path.isdir(carousel_folder):
        #     files = os.listdir(carousel_folder)
        #     for file in files:
        #         slide = {
        #             'image': 'static/{}/{}'.format('d1cc7584-eb2e-4394-8ac0-28906bc844d2', file),
        #             'index': index_
        #         }
        #         slides.append(slide)
        #         index_ += 1

        # retrieve the expected role for this section
        role = role_repository.find_by_id(section['rle_id'])

        posting = {
            'section': section['uuid'],
            'section_role': role['role']
        }

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
        return render_template('index/index.html', sections=sections, code=code, activities=activities,
                               posting=posting, slides=slides, clips=clips)
