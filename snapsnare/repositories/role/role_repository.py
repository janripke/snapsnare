from snapsnare.repositories.dataclass_repository import DataclassRepository


class RoleRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'roles')
