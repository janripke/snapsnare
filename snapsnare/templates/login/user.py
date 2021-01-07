from flask_login import UserMixin
from snapsnare.system import hasher


class User(UserMixin):
    def __init__(self, id_, username, password):
        UserMixin.__init__(self)
        self.id = id_
        self.username = username
        self.password = password

    def get_id(self):
        return self.id
        # return str(self.id, encoding='utf-8')

    # Password is stored as SHA512 string.
    def check_password(self, password):
        password = hasher.sha256(password)
        if password == self.password:
            return True
        return False
