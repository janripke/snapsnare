from snapsnare.repositories.dataclass_repository import DataclassRepository


class SectionComponentRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'section_components')
