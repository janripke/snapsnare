from paprika_connector.connectors.repository import Repository


class PropertyRepository(Repository):
    FIND_BY_NAME = 'application_properties_find_by_name.sql'
    INSERT = 'application_properties_insert.sql'
    INSERTS = 'application_properties_inserts.sql'
    VALUE = 'application_properties_value.sql'
    LIST = 'application_properties_list.sql'

    def find_by_name(self, name):
        # with self.get_connection() as cursor:
        statement = self._load(PropertyRepository.FIND_BY_NAME)

        params = dict()
        params['name'] = name

        return self._find(statement, params)

    def insert(self, property):
        statement = self._load(PropertyRepository.INSERT)
        return self._insert(statement, property)

    def inserts(self, properties):
        statement = self._load(PropertyRepository.INSERTS)
        self._inserts(statement, properties)

    def value(self, name, default=None):
        statement = self._load(PropertyRepository.VALUE)

        params = dict()
        params['name'] = name

        result = self._find(statement, params)
        if result is None:
            return default

        return result['value']

    def list(self):
        statement = self._load(PropertyRepository.LIST)

        params = dict()
        return self._list(statement, params)
