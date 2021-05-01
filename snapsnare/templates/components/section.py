import json
from flask import request, current_app
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section_component.section_component_repository import SectionComponentRepository


def load():
    # retrieve the uuid of the section
    uuid_ = request.args.get('section')
    connector = current_app.connector
    section_repository = SectionRepository(connector)
    section = section_repository.find_by_uuid(uuid_)
    if not section:
        # no uuid_ is given, so Home is assumed
        section = section_repository.find_by_name('Home')

    # retrieve the expected role for this section
    role_repository = RoleRepository(connector)
    role = role_repository.find_by_id(section['rle_id'])
    section['role'] = role['role']

    section_component_repository = SectionComponentRepository(connector)
    section_components = section_component_repository.list_by(stn_id=section['id'])

    components = []
    for section_component in section_components:
        components.append(section_component['component'])

    section['components'] = components

    return section
