from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter


class ActivityRepository(Repository):
    FIND_BY_UUID = 'activities_find_by_uuid.sql'
    LIST = 'activities_list.sql'
    LIST_BY_STN_ID = 'activities_list_by_stn_id.sql'
    INSERT = 'activities_insert.sql'

    def find_by_uuid(self, uuid_):
        # with self.get_connection() as cursor:
        statement = self._load(ActivityRepository.FIND_BY_UUID)

        params = {
            'uuid': uuid_
        }
        return self._find(statement, params)

    def list(self):
        statement = self._load(ActivityRepository.LIST)

        params = {}
        return self._list(statement, params)

    def list_by_stn_id(self, stn_id):
        statement = self._load(ActivityRepository.LIST_BY_STN_ID)

        params = {
            'stn_id': stn_id
        }
        return self._list(statement, params)

    def insert(self, activity):
        # if the uuid is not given, generate it.
        uuid_ = activity.get('uuid', str(uuid4()))

        params = {
            'uuid': uuid_,
            'usr_id': activity['usr_id'],
            'stn_id': activity['stn_id'],
            'content': activity['content'],
            'rendering': activity['rendering']
        }

        statement = self._load(ActivityRepository.INSERT)
        return self._insert(statement, params)

    def update(self, activity):
        connector = self.get_connector()
        cursor = connector.cursor()

        excludes = ['id', 'uuid']
        statement = 'update activities set {} where uuid=:uuid'.format(
            set_formatter(activity, excludes))

        statement, parameters = self.statement(statement, activity)
        cursor.execute(statement, parameters)
