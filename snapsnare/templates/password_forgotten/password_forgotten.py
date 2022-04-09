from uuid import uuid4
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app

from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.reset.reset_repository import ResetRepository
from snapsnare.repositories.template.template_repository import TemplateRepository
from snapsnare.system import utils, gmail

password_forgotten = Blueprint('password_forgotten', __name__, template_folder='templates')


@password_forgotten.route('/password_forgotten', methods=['POST', 'GET'])
def show():
    connector = current_app.connector

    if request.method == 'GET':
        section_repository = SectionRepository(connector)
        sections = section_repository.list_by(active=1, order_by='id')
        connector.close()
        return render_template('password_forgotten/password_forgotten.html', sections=sections)

    if request.method == 'POST':
        username = request.form['username']

        user_repository = UserRepository(connector)
        user = user_repository.find_by(username=username, active=1)

        if not user:
            flash('Invalid account state', 'danger')
            return redirect(url_for('login.show'))

        # disable previous resets of this user.
        reset = {
            "active": 0
        }
        reset_repository = ResetRepository(connector)
        reset_repository.update(reset, where={"username": user["username"]})

        # create an active reset for this user.
        reset = {
            "active": 1,
            "uuid": str(uuid4()),
            "username": user["username"],
        }
        reset_repository.insert(reset)

        properties = current_app.properties
        settings = utils.load_json(properties, 'snapsnare.json')
        credentials = settings['gmail']
        snapsnare = settings['snapsnare']
        host = snapsnare['host']

        template_repository = TemplateRepository(connector)
        template = template_repository.find_by(template='reset')
        content = template['content']
        content = content.replace("{host}", host)
        content = content.replace("{uuid}", reset['uuid'])

        connector.commit()

        gmail.send_email(credentials, reset['username'], "Reset your account on snapsnare.org", content)

        flash('A reset request is successfully created. Please check your e-mail to reset your password.', 'success')
        return redirect(url_for('login.show'))
