from snapsnare.repositories.dataclass_repository import DataclassRepository


class RegistrationRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'registrations')

    def is_registered(self, username):
        user = self.find_by(username=username, active=1)
        if user:
            return True
        return False
