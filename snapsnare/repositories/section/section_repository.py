from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter


class SectionRepository(Repository):
    FIND_BY_NAME = 'sections_find_by_name.sql'
    FIND_BY_UUID = 'sections_find_by_uuid.sql'
    LIST = 'sections_list.sql'
    INSERT = 'sections_insert.sql'

    def find_by_name(self, name):
        # with self.get_connection() as cursor:
        statement = self._load(SectionRepository.FIND_BY_NAME)

        params = {
            'name': name
        }
        return self._find(statement, params)

    def find_by_uuid(self, uuid_):
        # with self.get_connection() as cursor:
        statement = self._load(SectionRepository.FIND_BY_UUID)

        params = {
            'uuid': uuid_
        }
        return self._find(statement, params)

    def list(self):
        statement = self._load(SectionRepository.LIST)

        params = {
        }
        return self._list(statement, params)

    def update(self, section):
        connector = self.get_connector()
        cursor = connector.cursor()

        excludes = ['id', 'uuid']
        statement = 'update sections set {} where uuid=:uuid'.format(
            set_formatter(section, excludes))

        statement, parameters = self.statement(statement, section)
        cursor.execute(statement, parameters)

    def insert(self, section):
        # if the uuid is not given, generate it.
        uuid_ = section.get('uuid', str(uuid4()))

        params = {
            'uuid': uuid_,
            'name': section['name'],
            'endpoint': section['endpoint'],
            'url': section['url'],
            'rle_id': section['rle_id'],
            'nav_ind': section['nav_ind']
        }

        statement = self._load(SectionRepository.INSERT)
        return self._insert(statement, params)
