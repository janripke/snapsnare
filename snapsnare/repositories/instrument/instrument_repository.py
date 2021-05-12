from snapsnare.repositories.dataclass_repository import DataclassRepository


class InstrumentRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'instruments')
