from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter
from snapsnare.system import hasher


class UserRepository(Repository):
    FIND_BY_UUID = 'users_find_by_uuid.sql'
    FIND_BY_ID = 'users_find_by_id.sql'
    FIND_BY_USERNAME = 'users_find_by_username.sql'
    FIND_BY_RGN_ID = 'users_find_by_rgn_id.sql'
    INSERT = 'users_insert.sql'

    def find_by_uuid(self, uuid_):
        statement = self._load(UserRepository.FIND_BY_UUID)

        params = {
            'uuid': uuid_
        }

        return self._find(statement, params)

    def find_by_id(self, id_):
        statement = self._load(UserRepository.FIND_BY_ID)

        params = {
            'id': id_
        }

        return self._find(statement, params)

    def find_by_username(self, username):
        statement = self._load(UserRepository.FIND_BY_USERNAME)

        params = {
            'username': username
        }

        return self._find(statement, params)

    def find_by_rgn_id(self, rgn_id):
        statement = self._load(UserRepository.FIND_BY_RGN_ID)

        params = {
            'rgn_id': rgn_id
        }

        return self._find(statement, params)

    def insert(self, user):
        # if the uuid is not given, generate it.
        uuid_ = user.get('uuid', str(uuid4()))

        params = {
            'uuid': uuid_,
            'username': user['username'],
            'password': user['password'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'nickname': user['nickname'],
            'phone_number': user['phone_number'],
            'rle_id': user['rle_id'],
            'rgn_id': user['rgn_id']
        }

        statement = self._load(UserRepository.INSERT)
        return self._insert(statement, params)

    def update(self, user):
        connector = self.get_connector()
        cursor = connector.cursor()

        excludes = ['id', 'uuid']
        statement = 'update users set {} where uuid=:uuid'.format(
            set_formatter(user, excludes))

        statement, parameters = self.statement(statement, user)
        cursor.execute(statement, parameters)
