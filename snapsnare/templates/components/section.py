from flask import current_app
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.section_component.section_component_repository import SectionComponentRepository
from snapsnare.system import component


def load():
    connector = current_app.connector

    section = component.section()

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
