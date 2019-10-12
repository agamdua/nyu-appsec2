class Users(dict):
    def create(self, user):
        if user.username in self:
            raise UniqueConstraintError
        return self._save(user)

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
    def __init__(self, username, password):
        this.username = username
        this.password = password


class UniqueConstraintError(Exception): pass
class UserDoesNotExist(Exception): pass

test_user = User('test', 'test')
