from enum import Enum
from flask import request, current_app
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.component.component_repository import ComponentRepository
from snapsnare.repositories.fragment.fragment_repository import FragmentRepository


class ComponentEnum(Enum):
    ACTIVITIES = "activities"
    JAMMERS = "jammers"
    MY_SAMPLES = "my_samples"
    POSTING = "posting"
    SAMPLES = "samples"
    SIDEBAR = "sidebar"
    UPLOAD = "upload"


def section():
    connector = current_app.connector
    section_repository = SectionRepository(connector)

    uuid_ = request.args.get('section')
    section_ = section_repository.find_by_uuid(uuid_)

    if not section_:
        # no uuid_ is given, so Home is assumed
        section_ = section_repository.find_by(name='Home', active=1)

    return section_


def has_fragment(section: dict, component: ComponentEnum):
    connector = current_app.connector
    fragment_repository = FragmentRepository(connector)
    component_repository = ComponentRepository(connector)

    component_ = component_repository.find_by(component=component.value)
    if component_:
        if section:
            # check if this component is configured for this section
            fragments = fragment_repository.list_by(stn_id=section['id'])
            for fragment in fragments:
                if fragment['cpt_id'] == component_['id']:
                    return True
    return False
