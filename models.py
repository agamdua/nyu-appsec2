import enum

from flask_login import UserMixin

from app import db


class Roles(enum.Enum):
    admin = "admin"
    user = "user"


class User(UserMixin, db.Model):

    __tablename__ = "cuser"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    role = db.Column(db.Enum(Roles))
    two_factor = db.Column(db.String(80))

    is_anonymous = False

    def __init__(self, username, password, role=Roles.user, two_factor=""):
        self.username = username
        self.password = password
        self.role = role
        self.two_factor = two_factor

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def create_session(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    @property
    def is_admin(self):
        return True if self.role == Roles.admin else False


class SpellCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_to_check = db.Column(db.Text())
    result = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey("cuser.id"))
    user = db.relationship("User")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


def create_database_users():
    test_user = User(username="test", password="test", role=Roles.admin)
    test_user.save()

    admin_user = User(
        username="admin", password="Administrator@1", two_factor="12345678901"
    )
    admin_user.save()
