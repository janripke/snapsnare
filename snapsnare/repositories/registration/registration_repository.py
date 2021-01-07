from uuid import uuid4
from snapsnare.system import hasher
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter


class RegistrationRepository(Repository):
    INSERT = 'registrations_insert.sql'
    FIND_BY_USERNAME = 'registrations_find_by_username.sql'
    FIND_BY_UUID = 'registrations_find_by_uuid.sql'
    FIND_BY_ID = 'registrations_find_by_id.sql'
    LIST = 'registrations_list.sql'

    def is_registered(self, username):
        user = self.find_by_username(username)
        if user:
            return True
        return False

    def find_by_username(self, username):
        statement = self._load(RegistrationRepository.FIND_BY_USERNAME)

        params = {
            'username': username
        }

        return self._find(statement, params)

    def find_by_uuid(self, uuid_):
        statement = self._load(RegistrationRepository.FIND_BY_UUID)

        params = {
            'uuid': uuid_
        }

        return self._find(statement, params)

    def find_by_id(self, id_):
        statement = self._load(RegistrationRepository.FIND_BY_ID)

        params = {
            'id': id_
        }

        return self._find(statement, params)

    def insert(self, registration):
        # if the uuid is not given, generate it.
        uuid_ = registration.get('uuid', str(uuid4()))

        # if the password is given encrypt it.
        # fixme: only if the password is given hash it.
        password = hasher.sha256(registration.get('password'))

        params = {
            'uuid': uuid_,
            'username': registration['username'],
            'password': password,
            'first_name': registration['first_name'],
            'last_name': registration['last_name'],
            'rle_id': registration['rle_id']
        }

        statement = self._load(RegistrationRepository.INSERT)
        return self._insert(statement, params)

    def list(self):
        statement = self._load(RegistrationRepository.LIST)

        params = {
        }
        return self._list(statement, params)

    def update(self, registration):
        connector = self.get_connector()
        cursor = connector.cursor()

        excludes = ['id', 'uuid']
        statement = 'update registrations set {} where uuid=:uuid'.format(
            set_formatter(registration, excludes))

        statement, parameters = self.statement(statement, registration)
        cursor.execute(statement, parameters)
