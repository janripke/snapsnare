from snapsnare.repositories.dataclass_repository import DataclassRepository


class UserRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'resets')

    def find_by_username(self, username):
        return self.find_by(username=username, active=1)