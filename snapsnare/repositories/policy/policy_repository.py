from snapsnare.repositories.dataclass_repository import DataclassRepository


class PolicyRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'policies')
