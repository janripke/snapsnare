from snapsnare.repositories.dataclass_repository import DataclassRepository


class ResetRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'resets')
