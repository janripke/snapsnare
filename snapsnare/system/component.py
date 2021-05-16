from enum import Enum
from flask import request, current_app
from snapsnare.repositories.section.section_repository import SectionRepository
from snapsnare.repositories.section_component.section_component_repository import SectionComponentRepository


class SectionComponent(Enum):
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
        section_ = section_repository.find_by_name('Home')

    return section_


def has_section_component(section: dict, component: SectionComponent):
    connector = current_app.connector
    section_component_repository = SectionComponentRepository(connector)

    if section:
        # check if this component is configured for this section
        section_components = section_component_repository.list_by(stn_id=section['id'])
        for section_component in section_components:
            if section_component['component'] == component.value:
                return True
    return False
