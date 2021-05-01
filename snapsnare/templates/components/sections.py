from flask import current_app
from snapsnare.repositories.section.section_repository import SectionRepository


def load():
    # retrieve the sections to show in the navbar
    connector = current_app.connector
    section_repository = SectionRepository(connector)
    return section_repository.list()
