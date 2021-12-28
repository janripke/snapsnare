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
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section.section_repository import SectionRepository
profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    user_repository = UserRepository(connector)
    section_repository = SectionRepository(connector)

    sections = section_repository.list_by(active=1, order_by='id')

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')

        # check messing with uuid's
        if uuid_ != session['uuid']:
            return redirect(url_for('login.show'))

        user = user_repository.find_by_uuid(uuid_)
        user = dictionaries.strip_none(user)

        role_repository = RoleRepository(connector)
        role = role_repository.find_by(id=user['rle_id'], active=1)
        user['role'] = role['role']

        connector.close()
        return render_template('profile/profile.html', sections=sections, user=user)

    uuid_ = request.form['uuid']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    nickname = request.form['nickname']
    phone_number = request.form['phone_number']

    user = {
        'uuid': uuid_,
        'first_name': first_name,
        'last_name': last_name,
        'nickname': nickname,
        'phone_number': phone_number
    }

    # check messing with uuid's
    if uuid_ != session['uuid']:
        return redirect(url_for('login.show'))

    user_repository.update(user)
    user = user_repository.find_by_uuid(user['uuid'])
    connector.commit()
    connector.close()
    flash('Je profielgegevens zijn bijgewerkt', 'info')
    return render_template('profile/profile.html', sections=sections, user=user)



