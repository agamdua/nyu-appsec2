from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)

    is_anonymous = False

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(int(user_id))

    def get(self):
        if self.id is not None:
            return self.__class__.get_by_id(int(self.id))
        return self.__class__.query.filter_by(username=self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def create_session(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False


# spell_check_submissions = db.Table('spell_checks',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     db.Column('spell_check_id', db.Integer, db.ForeignKey('spell_check.id'), primary_key=True)
# )


class SpellCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_to_check = db.Column(db.Text())
    result = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")
