from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask import session
from flask_login import login_required

from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.system import dictionaries
from snapsnare.templates.login.user import User
from snapsnare.system import hasher

password = Blueprint('password', __name__, template_folder='templates')


@password.route('/password', methods=['GET', 'POST'])
@login_required
def show():
    connector = current_app.connector
    user_repository = UserRepository(connector)

    if request.method == 'GET':
        uuid_ = request.args.get('uuid')
        if uuid_ != session['uuid']:
            return redirect(url_for('login.show'))

        user = user_repository.find_by_uuid(uuid_)
        user = dictionaries.strip_none(user)

        section_repository = SectionRepository(connector)
        sections = section_repository.list_by(active=1, order_by='id')

        connector.close()
        return render_template('password/password.html', sections=sections, user=user)

    uuid_ = request.form['uuid']
    password_ = request.form['password']
    new_password = request.form['new_password']
    repeat = request.form['repeat']

    if uuid_ != session['uuid']:
        return redirect(url_for('login.show'))

    user = user_repository.find_by_username(session['username'])
    if not user:
        flash('Invalid username.', 'danger')
        return redirect(url_for('password.show', uuid=uuid_))

    registered_user = User(user['uuid'], user['username'], user['password'])
    if not registered_user.check_password(password_):
        flash('Invalid password.', 'error')
        return redirect(url_for('password.show', uuid=uuid_))

    # the given passwords do not match
    if new_password != repeat:
        flash('The newly entered passwords do not match.', 'danger')
        return redirect(url_for('password.show', uuid=uuid_))

    # change the password
    user = {
        'uuid': uuid_,
        'password': hasher.sha256(new_password)
    }
    user_repository.update(user)
    connector.commit()
    connector.close()

    # show the login screen
    flash('The password is updated successfully.', 'success')
    return redirect(url_for('password.show', uuid=uuid_))
