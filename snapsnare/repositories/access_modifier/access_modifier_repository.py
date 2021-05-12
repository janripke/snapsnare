from snapsnare.repositories.dataclass_repository import DataclassRepository


class AccessModifierRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'access_modifiers')

