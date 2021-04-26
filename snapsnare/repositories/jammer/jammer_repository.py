from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter
from snapsnare.repositories.dataclass_repository import DataclassRepository


class JammerRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'jammers')
