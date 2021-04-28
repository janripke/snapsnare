from snapsnare.repositories.dataclass_repository import DataclassRepository


class IcecastStatusRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'icecast_statuses')
