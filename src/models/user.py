from src.common.database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid


class User(UserMixin):

    def __init__(self, username, password_hash, _id=None):
        self.username = username
        self.password_hash = password_hash
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_id(self):
        return self._id

    def save_to_mongo(self):
        Database.insert(collection='admin_users', data=self.json())

    def json(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            '_id': self._id
        }

    def set_password(self, new_password):
        self.password_hash = generate_password_hash(new_password)
        query = {'_id': self._id}
        new_pw = {'password_hash': self.password_hash}
        Database.update_one(collection='admin_users', query=query, new_vals={'$set': new_pw})

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user(cls, username):
        user = Database.find_one(collection='admin_users', query={'username': username})
        return cls(**user)

    @classmethod
    def get_user_by_id(cls, id):
        user = Database.find_one(collection='admin_users', query={'_id': id})
        return cls(**user)

    @staticmethod
    def add_admin():
        user = User("Admin", "pbkdf2:sha256:150000$tOEO8zuZ$7529b7ee8596fc45e20527cd54802df0357e721ed09ecc795aeb83a34c6414d4")
        user.save_to_mongo()
