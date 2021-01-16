from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter


class SnapRepository(Repository):
    FIND_BY_UUID = 'snaps_find_by_uuid.sql'
    LIST = 'snaps_list.sql'
    INSERT = 'snaps_insert.sql'

    def find_by_uuid(self, uuid_):
        # with self.get_connection() as cursor:
        statement = self._load(SnapRepository.FIND_BY_UUID)

        params = {
            'uuid': uuid_
        }
        return self._find(statement, params)

    def list(self):
        statement = self._load(SnapRepository.LIST)

        params = {}
        return self._list(statement, params)

    def insert(self, snap):
        # if the uuid is not given, generate it.
        uuid_ = snap.get('uuid', str(uuid4()))

        params = {
            'uuid': uuid_,
            'usr_id': snap['usr_id'],
            'title': snap['title']
        }

        statement = self._load(SnapRepository.INSERT)
        return self._insert(statement, params)

    def update(self, snap):
        connector = self.get_connector()
        cursor = connector.cursor()

        excludes = ['id', 'uuid']
        statement = 'update snaps set {} where uuid=:uuid'.format(
            set_formatter(snap, excludes))

        statement, parameters = self.statement(statement, snap)
        cursor.execute(statement, parameters)
