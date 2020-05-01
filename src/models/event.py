import uuid
from datetime import datetime, date

from common.database import Database


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
        #Convert date/time to datetime object

    def save_to_mongo(self):
        Database.insert(collection='pending_events',
                        data=self.json())
    def approve(self):
        q = { '_id': self._id}
        Database.delete_one(collection='pending_events', query=q)
        Database.insert(collection='approved_events', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'email': self.email,
            'title': self.title,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'description': self.description
        }

    def date_time(self):
        cur_date = date.fromisoformat(self.date)
        cur_time = datetime.strptime(self.time, "%H:%M").time()
        dt = datetime.combine(cur_date, cur_time)
        return dt.strftime("%b %d @ %I:%M %p")

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
        posts = Database.find(collection='pending_events', query={})
        return [cls(**post) for post in posts]