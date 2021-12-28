from snapsnare.repositories.dataclass_repository import DataclassRepository


class FragmentAssignmentRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'fragment_assignments')
