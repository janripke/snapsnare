from paprika_connector.connectors.repository import Repository


class RoleRepository(Repository):
    FIND_BY_ID = 'roles_find_by_id.sql'
    FIND_BY_ROLE = 'roles_find_by_role.sql'
    LIST = 'roles_list.sql'

    def find_by_id(self, id_):
        # with self.get_connection() as cursor:
        statement = self._load(RoleRepository.FIND_BY_ID)

        params = {
            'id': id_
        }
        return self._find(statement, params)

    def find_by_role(self, role):
        # with self.get_connection() as cursor:
        statement = self._load(RoleRepository.FIND_BY_ROLE)

        params = {
            'role': role
        }
        return self._find(statement, params)

    def list(self):
        statement = self._load(RoleRepository.LIST)

        params = {
        }
        return self._list(statement, params)