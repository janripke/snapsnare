import os
from uuid import uuid4
from pathlib import Path

import click
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_login import logout_user
from flask import redirect
from flask import url_for
from flask import session

import snapsnare
from paprika_connector.connectors.connector_factory import ConnectorFactory
from snapsnare.repositories.user.user_repository import UserRepository
from snapsnare.system import utils

from snapsnare.rest.auth.auth import Auth
from snapsnare.rest.properties.show_property import ShowProperty

from snapsnare.templates.index.index import index
from snapsnare.templates.register.register import register
from snapsnare.templates.profile.profile import profile
from snapsnare.templates.settings.settings import settings
from snapsnare.templates.registrations.registrations import registrations
from snapsnare.templates.activate.activate import activate
from snapsnare.templates.reject.reject import reject
from snapsnare.templates.recover.recover import recover
from snapsnare.templates.block.block import block
from snapsnare.templates.release.release import release
from snapsnare.templates.terminate.terminate import terminate
from snapsnare.templates.registration.registration import registration
from snapsnare.templates.password.password import password
from snapsnare.templates.posting.posting import posting
from snapsnare.templates.sections.sections import sections
from snapsnare.templates.section.section import section
from snapsnare.templates.login.login import login
from snapsnare.templates.login.user import User

application = Flask(__name__)
api = Api(application)

properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}

ds = utils.load_json(properties, 'snapsnare-ds.json')

connector = ConnectorFactory.create_connector(ds)
application.connector = connector
application.properties = properties

# set the secret, jwt uses this.
# every time the rest server start a new secret is created. Sessions do not survive a reboot.
application.config['SECRET_KEY'] = uuid4().hex

# set the upload folder
application.config['UPLOAD_FOLDER'] = os.path.join(properties['package.dir'], 'static')


# initialize the logger
utils.load_logger(properties, 'log.json', 'snapsnare')

# initialize jwt
application.config['JWT_SECRET_KEY'] = uuid4().hex
jwt = JWTManager(application)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login.show'

api.add_resource(Auth, '/auth')
api.add_resource(ShowProperty, '/properties/show')

application.register_blueprint(index)
application.register_blueprint(register)
application.register_blueprint(login)
application.register_blueprint(profile)
application.register_blueprint(settings)
application.register_blueprint(registrations)
application.register_blueprint(activate)
application.register_blueprint(reject)
application.register_blueprint(recover)
application.register_blueprint(block)
application.register_blueprint(release)
application.register_blueprint(terminate)
application.register_blueprint(registration)
application.register_blueprint(password)
application.register_blueprint(posting)
application.register_blueprint(sections)
application.register_blueprint(section)


@login_manager.user_loader
def load_user(user_id):
    user_repository = UserRepository(connector)
    user = user_repository.find_by_uuid(user_id)
    connector.close()
    if not user:
        return redirect(url_for('login.show'))
    else:
        return User(user['id'], user['username'], user['password'])


@application.route('/logout')
def logout():
    logout_user()

    # remove the session variables for the user
    session.pop('username')
    session.pop('uuid')
    session.pop('role')
    return redirect(url_for('index.show'))


@click.command()
@click.option('-d', '--debug', required=False, default=False, is_flag=True)
@click.option('-p', '--port', required=False, type=int, default=5000)
@click.option('-h', '--host', required=False, default='0.0.0.0')
def main(debug, port, host):
    application.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    main(args=None)
