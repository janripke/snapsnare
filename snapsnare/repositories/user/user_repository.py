from snapsnare.repositories.dataclass_repository import DataclassRepository


class UserRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'users')

    def find_by_username(self, username):
        return self.find_by(username=username, active=1)

    def find_by_rgn_id(self, rgn_id):
        return self.find_by(rgn_id=rgn_id, active=1)
