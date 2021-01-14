from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import current_app
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_required


from snapsnare.system import dictionaries
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.role.role_repository import RoleRepository

section = Blueprint('section', __name__, template_folder='templates')


@section.route('/section', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    section_repository = SectionRepository(connector)
    role_repository = RoleRepository(connector)

    sections = section_repository.list()

    role = session.get('role', 'user')
    if role != 'admin':
        return redirect(url_for('login.show'))

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')

        roles = role_repository.list()

        if uuid_:
            section_ = section_repository.find_by_uuid(uuid_)
            section_ = dictionaries.strip_none(section_)

            role = role_repository.find_by_id(section_['rle_id'])
            section_['role'] = role['role']

            connector.close()
            return render_template('section/section.html', sections=sections, section=section_, roles=roles)

        section_ = {
        }

        return render_template('section/section.html', sections=sections, section=section_, roles=roles)

    if request.method == 'POST':
        uuid_ = request.form['uuid']
        name = request.form['name']
        endpoint = request.form['endpoint']
        url = request.form['url']
        role = request.form['role']
        nav_ind = request.form.get('nav_ind', 0)
        role = role_repository.find_by_role(role)

        if uuid_:
            section_ = {
                'uuid': uuid_,
                'name': name,
                'endpoint': endpoint,
                'url': url,
                'rle_id': role['id'],
                'nav_ind': nav_ind
            }
            section_repository.update(section_)

            connector.commit()
            connector.close()
            flash('De sectie details zijn bijgewerkt.', 'info')
            return redirect(url_for('sections.show'))

        section_ = {
            'name': name,
            'endpoint': endpoint,
            'url': url,
            'rle_id': role['id'],
            'nav_ind': nav_ind
        }

        section_repository.insert(section_)
        connector.commit()
        connector.close()
        flash('De sectie is toegevoegd.', 'info')
        return redirect(url_for('sections.show'))
