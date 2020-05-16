from src.common.database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid


class User(UserMixin):
    """ User system being used to create admin accounts for approval process"""

    def __init__(self, username, password_hash, _id=None):
        self.username = username
        self.password_hash = password_hash
        self._id = uuid.uuid4().hex if _id is None else _id

    def get_id(self):
        """
        Returns the id associated with a user

        :return: (string) user's id
        """
        return self._id

    def save_to_mongo(self):
        """ Inserts the user into the database """
        Database.insert(collection='admin_users', data=self.json())

    def json(self):
        """
        Method that converts the class into a json-format that can be stored in the database

        :return: (dictionary) used for submitting User to database
         """
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            '_id': self._id
        }

    def set_password(self, new_password):
        """
        Changes the password associated with the user in the database

        :param new_password: (string) the new password
        """

        self.password_hash = generate_password_hash(new_password)
        query = {'_id': self._id}
        new_pw = {'password_hash': self.password_hash}
        Database.update_one(collection='admin_users', query=query, new_vals={'$set': new_pw})


    def check_password(self, password):
        """
        Takes in a password when trying to login, hashes it, and checks it matches the one in the database.

        :param password: (string) password entered
        :return: (boolean) whether the password matches the one in the database or not
        """
        return check_password_hash(self.password_hash, password)


    @classmethod
    def get_user(cls, username):
        """
        Gets a user from the database using their associated username

        :param username: (string) the username of the user you're trying to retrieve
        :return: (User) the corresponding user
        """
        user = Database.find_one(collection='admin_users', query={'username': username})
        return cls(**user)

    @classmethod
    def get_user_by_id(cls, id):
        """
        Gets a user from the database using their associated id

        :param id: (string) the id of the user you're trying to retrieve
        :return: (User) the corresponding user
        """
        user = Database.find_one(collection='admin_users', query={'_id': id})
        return cls(**user)

    @staticmethod
    def add_admin():
        """ Creates an admin account with a default password and stores it in the database """
        print("Hit")
        user = User("Admin", generate_password_hash("admin123"))
        user.save_to_mongo()
