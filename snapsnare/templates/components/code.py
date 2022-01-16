from flask import current_app
import snapsnare
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.property.property_repository import PropertyRepository


def load():
    connector = current_app.connector
    section_repository = SectionRepository(connector)
    property_repository = PropertyRepository(connector)
    about = section_repository.find_by(name='About us', active=1)
    team = section_repository.find_by(name='Team', active=1)

    code = {
        'name': snapsnare.__name__,
        'version': snapsnare.__version__,
        'about': about['uuid'],
        'team': team['uuid']
    }

    environment = property_repository.find_by(name='application.environment')
    code['environment'] = environment.get('value')

    backend_version = property_repository.find_by(name='application.version')
    backend = {
        'version': backend_version.get('value')
    }

    code['backend'] = backend
    return code
