import uuid
from datetime import datetime

from src.common.database import Database
#from common.database import Database


class Trailer(object):
    """ Trailers submitted by students to be displayed on the board """

    def __init__(self, author, email, display_email, title, trailer_path, date=datetime.now(), link=None, _id=None):
        self.author = author
        self.email = email
        self.display_email = display_email
        self.title = title
        self.trailer_path = trailer_path
        self.date = date
        self.link = link
        self._id = uuid.uuid4().hex if _id is None else _id

    # Note: If using own collection, add quotes when calling this method, as it takes a string.
    def save_to_mongo(self, collection='pending_trailers'):
        """ Save self to database as a 'pending_trailer' to await for approval"""
        Database.insert(collection=collection, data=self.json())

    def json(self):
        """
        Method that converts the class into a json-format that can be stored in the database

        :return: (dictionary) used for submitting Trailer to database
        """
        return {
            'author': self.author,
            'email': self.email,
            'display_email': self.display_email,
            'title': self.title,
            'trailer_path': self.trailer_path,
            'date': self.date,
            'link': self.link,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        """ :return: (Trailer) corresponding to the entry in the database with the same id"""
        post_data = Database.find_one(collection='pending_trailers', query={'_id': id})
        return cls(**post_data)

    @classmethod
    def move(cls, entry, collection1, collection2):
        """Moves an entry from one collection to another

        :param entry: (Trailer) the item we want to move
        :param collection1: (string) collection where the entry currently exists
        :param collection2: (string) collection we want to move the entry to"""
        entry.save_to_mongo(collection=collection2)
        Database.delete_one(collection=collection1, query={'id': entry._id})

    @classmethod
    def get_all(cls, collection):
        """
        Get a list of all trailers in a specific collection

        :param collection: (string) name of the collection we are looking at
        :return: (list) consisting of Trailers from the database
        """
        trailers = Database.find(collection=collection, query={})
        return [cls(**trailer) for trailer in trailers]

    # Following 3 methods are vestigial until we can refactor them out.
    @classmethod
    def get_pending(cls):
        trailers = Database.find(collection='pending_trailers', query={})
        return [cls(**trailer) for trailer in trailers]

    @classmethod
    def get_queued(cls):
        trailers = Database.find(collection='queued_trailers', query={})
        return [cls(**trailer) for trailer in trailers]

    @classmethod
    def get_approved(cls):
        trailers = Database.find(collection='approved_trailers', query={})
        return [cls(**trailer) for trailer in trailers]

    @classmethod
    def approve(cls, id):
        """
        Approves a trailer, moving it from one pending_trailers to queued_trailers

        :param id: (string) id of the corresponding entry in the database
        """
        q = {'_id': id}
        post = Database.find_one(collection='pending_trailers', query=q)
        Database.insert(collection='queued_trailers', data=post)
        Database.delete_one(collection='pending_trailers', query=q)

    @classmethod
    def deny(cls, id):
        """
        Denies a trailer, removing it from the pending_trailers

        :param id: (string) id of the corresponding entry in the database
        """
        q = {'_id': id}
        Database.delete_one(collection='pending_trailers', query=q)

    @classmethod
    def remove_expired(cls):
        """ Iterates through all Trailers in the database, replacing those that have been in rotation for longer than 2
        weeks with ones in the queue if they exist. Removed trailers are sent to the archived_trailers collection in
        case someone wants to repurpose them in the future."""
        max_trailers = 10
        current_trailers = cls.get_all(collection='approved_trailers')
        current_trailers.reverse()
        queued_trailers = cls.get_all(collection='queued_trailers')

        if len(current_trailers) >= max_trailers and len(queued_trailers) > 0:
            for trailer in current_trailers:
                time_active = trailer.date.timetuple().tm_yday - datetime.now().timetuple().tm_yday
                if time_active >= 14 and len(queued_trailers) > 0:
                    cls.move(trailer, 'approved_trailers', 'archived_trailers')
                    cls.move(queued_trailers[0], 'queued_trailers', 'approved_trailers')
