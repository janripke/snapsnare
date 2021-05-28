from snapsnare.repositories.dataclass_repository import DataclassRepository


class JammerRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'jammers')
