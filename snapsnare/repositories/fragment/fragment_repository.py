from snapsnare.repositories.dataclass_repository import DataclassRepository


class FragmentRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'fragments')
