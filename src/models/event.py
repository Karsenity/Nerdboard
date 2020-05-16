import uuid
from datetime import datetime, date

from src.common.database import Database
#from common.database import Database


class Event(object):

    def __init__(self, author, email, title, date, time, location, description, _id=None):
        self.author = author
        self.email = email
        self.title = title
        self.date = date
        self.time = time
        self.location = location
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='pending_events',
                        data=self.json())

    def expire(self):
        q = {'_id': self._id}
        Database.delete_one(collection='approved_events', query=q)

    def json(self):
        return {
            'author': self.author,
            'email': self.email,
            'title': self.title,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'description': self.description,
            '_id': self._id,
        }

    def date_time(self):
        cur_date = datetime.strptime(self.date, '%Y-%m-%d')
        cur_time = datetime.strptime(self.time, "%H:%M").time()
        dt = datetime.combine(cur_date, cur_time)
        return dt.strftime("%b %d @ %I:%M %p")

    def string_id(self):
        return str(self._id)

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='pending_events', query={'_id': id})
        return cls(**post_data)

    @classmethod
    def get_approved(cls):
        posts = Database.find(collection='approved_events', query={})
        return [cls(**post) for post in posts]

    @classmethod
    def get_pending(cls):
        events = Database.find(collection='pending_events', query={})
        return [cls(**event) for event in events]

    @classmethod
    def approve(cls, id):
        q = {'_id': id}
        post = Database.find_one(collection='pending_events', query=q)
        Database.insert(collection='approved_events', data=post)
        Database.delete_one(collection='pending_events', query=q)

    @classmethod
    def deny(cls, id):
        q = {'_id': id}
        Database.delete_one(collection='pending_events', query=q)

    @classmethod
    def remove_expired(cls):
        events = cls.get_approved()
        for event in events:
            event_date = datetime.strptime(event.date, '%Y-%m-%d')
            cur_date = datetime.now()
            if event_date < cur_date:
                event.expire()


