import uuid
from datetime import datetime

from src.common.database import Database
#from common.database import Database


class Trailer(object):

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
        Database.insert(collection=collection, data=self.json())

    def json(self):
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
        post_data = Database.find_one(collection='pending_trailers', query={'_id': id})
        return cls(**post_data)

    # Moves a trailer from one collection to another
    @classmethod
    def move(cls, entry, collection1, collection2):
        entry.save_to_mongo(collection=collection2)
        Database.delete_one(collection=collection1, query={'id': entry._id})

    @classmethod
    def get_all(cls, collection):
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
        q = {'_id': id}
        post = Database.find_one(collection='pending_trailers', query=q)
        Database.insert(collection='queued_trailers', data=post)
        Database.delete_one(collection='pending_trailers', query=q)

    @classmethod
    def deny(cls, id):
        q = {'_id': id}
        Database.delete_one(collection='pending_trailers', query=q)

    @classmethod
    def remove_expired(cls):
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
