from paprika_connector.connectors.repository import Repository


class InstrumentRepository(Repository):
    FIND_BY_ID = 'instruments_find_by_id.sql'
    FIND_BY_NAME = 'instruments_find_by_role.sql'
    LIST = 'instruments_list.sql'

    def find_by_id(self, id_):
        # with self.get_connection() as cursor:
        statement = self._load(InstrumentRepository.FIND_BY_ID)

        params = {
            'id': id_
        }
        return self._find(statement, params)

    def find_by_name(self, name):
        # with self.get_connection() as cursor:
        statement = self._load(InstrumentRepository.FIND_BY_NAME)

        params = {
            'name': name
        }
        return self._find(statement, params)

    def list(self):
        statement = self._load(InstrumentRepository.LIST)

        params = {
        }
        return self._list(statement, params)
