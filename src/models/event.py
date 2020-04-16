import uuid
from datetime import datetime, date

from common.database import Database


class Event(object):

    def __init__(self, author, email, title, date_val, time_val, location, description, _id=None):
        self.author = author
        self.email = email
        self.title = title
        self.date = date.fromisoformat(date_val)
        self.time = datetime.strptime(time_val, "%H:%M").time()
        self.location = location
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id
        #Convert date/time to datetime object
        self.date_time = datetime.combine(self.date, self.time)

    def save_to_mongo(self):
        Database.insert(collection='pending_events',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'email': self.email,
            'title': self.title,
            'date_time': self.date_time,
            'location': self.location,
            'description': self.description
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='pending_events', query={'_id': id})
        return cls(**post_data)
