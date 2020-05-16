import pymongo as pymongo


class Database(object):
    """ Basic methods to make interaction with MongoDB easier """

    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        """ inits the database to fullstack, and links to it based on the URI"""
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        """inserts a new entry into the specified collection

        :param collection: (string) name of the collection data will be saved to
        :param data: information in the format of a json-file
        """
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        """Finds all entries that contain the query within the database.

        :param collection: (string) name of the collection data will be saved to
        :param data: information in the format of a json-file
        :return: (dictionary) database entries matching query
        """
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        """Finds a specific value matching the query in the database.

        :param collection: (string) name of the collection data will be saved to
        :param data: information in the format of a json-file
        :return: (dictionary) SINGLE database entry matching query
        """
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_one(collection, query):
        """Finds a specific entry in the database, simultaneously returning it and removing it.

        :param collection: (string) name of the collection data will be saved to
        :param data: information in the format of a json-file
        :return: (dictionary) SINGLE database entry matching query, as well as removing it from database.
        """
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def update_one(collection, query, new_vals):
        """Updates entries in the database by replacing current values with new ones

        :param collection: (string) name of the collection data will be saved to
        :param data: information in the format of a json-file
        :param new_vals: (dictionary) Replacement values for matching entries in the database.
        """
        Database.DATABASE[collection].update_one(query, new_vals)

    @staticmethod
    def is_empty(collection):
        """ Returns boolean based on whether collection has been populated.

        :param collection: (string) name of the collection data will be saved to
        :return: (boolean) true when collection is empty
        """
        return Database.DATABASE[collection].count_documents({}) == 0

