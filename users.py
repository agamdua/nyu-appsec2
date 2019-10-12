class UniqueConstraintError(Exception): pass
class UserDoesNotExist(Exception): pass

class Users(dict):
    def create(self, user):
        if user.username in self:
            raise UniqueConstraintError
        return self._save(user)

    def get_by_id(self, user_id):
        return self.get(user_id)

    def get(self, user):
        try:
            fetched_user = self[user.username]
        except KeyError:
            raise UserDoesNotExist(user)

        return fetched_user

    def get_or_create(self, user):
        try:
            self.get(user)
        except UserDoesNotExist:
            pass
        
        return self.create(user)

    def _save(self, user):
        self[user.username] = user
        return user


class User:
    def __init__(self, username, password, is_authenticated=False, is_active=True, is_anonymous=True):
        self.username = username
        self.password = password
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = True

    def create_session():
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id():
        return self.username


test_user = User('test', 'test')
users = Users()
users.create(test_user)
