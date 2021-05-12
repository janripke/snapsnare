from snapsnare.repositories.dataclass_repository import DataclassRepository


class SnapRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'snaps')

