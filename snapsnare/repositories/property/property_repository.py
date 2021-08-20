from snapsnare.repositories.dataclass_repository import DataclassRepository


class PropertyRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'application_properties')
