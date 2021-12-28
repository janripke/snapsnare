from flask import current_app
from snapsnare.repositories.role.role_repository import RoleRepository
from snapsnare.repositories.fragment.fragment_repository import FragmentRepository
from snapsnare.repositories.component.component_repository import ComponentRepository
from snapsnare.system import component


def load():
    connector = current_app.connector

    section = component.section()

    # retrieve the expected role for this section
    role_repository = RoleRepository(connector)
    role = role_repository.find_by(id=section['rle_id'], active=1)
    section['role'] = role['role']

    fragment_repository = FragmentRepository(connector)
    component_repository = ComponentRepository(connector)
    fragments = fragment_repository.list_by(stn_id=section['id'], active=1)

    components = []
    for fragment in fragments:
        component_ = component_repository.find_by(id=fragment['cpt_id'], active=1)
        components.append(component_['component'])
    section['components'] = components

    allowed_roles = []
    if section['role'] == 'user':
        allowed_roles = ['user', 'moderator', 'admin']
    elif section['role'] == 'moderator':
        allowed_roles = ['moderator', 'admin']
    elif section['role'] == 'admin':
        allowed_roles = ['admin']
    section['allowed_roles'] = allowed_roles

    return section
