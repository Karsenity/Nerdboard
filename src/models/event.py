import uuid
from datetime import datetime, date

from src.common.database import Database
#from common.database import Database


class Event(object):
    """ Events submitted by students to be displayed on the board """

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
        """ Save self to database as a 'pending_event' to await for approval"""
        Database.insert(collection='pending_events',
                        data=self.json())

    def expire(self):
        """ Remove self from database """
        q = {'_id': self._id}
        Database.delete_one(collection='approved_events', query=q)

    def json(self):
        """
        Method that converts the class into a json-format that can be stored in the database

        :return: (dictionary) used for submitting an Event to the database
        """
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
        """ :returns: (string) Converts date and time into a readable format to be displayed """
        cur_date = datetime.strptime(self.date, '%Y-%m-%d')
        cur_time = datetime.strptime(self.time, "%H:%M").time()
        dt = datetime.combine(cur_date, cur_time)
        return dt.strftime("%b %d @ %I:%M %p")

    def string_id(self):
        return str(self._id)

    @classmethod
    def from_mongo(cls, id):
        """ :returns: (Event) Gets an event from the database using its id"""
        post_data = Database.find_one(collection='pending_events', query={'_id': id})
        return cls(**post_data)

    @classmethod
    def get_approved(cls):
        """:returns: (list) returns a list of all approved events"""
        posts = Database.find(collection='approved_events', query={})
        return [cls(**post) for post in posts]

    @classmethod
    def get_pending(cls):
        """:returns: (list) returns a list of all pending events"""
        events = Database.find(collection='pending_events', query={})
        return [cls(**event) for event in events]

    @classmethod
    def approve(cls, id):
        """ Takes in an id and removes it from pending_events, before adding it to approved_events
        :param id: (string)the id of the corresponding event in the database"""
        q = {'_id': id}
        post = Database.find_one(collection='pending_events', query=q)
        Database.insert(collection='approved_events', data=post)
        Database.delete_one(collection='pending_events', query=q)

    @classmethod
    def deny(cls, id):
        """ Takes in an id and removes it from pending_events
        :param id: (string)the id of the corresponding event in the database"""
        q = {'_id': id}
        Database.delete_one(collection='pending_events', query=q)

    @classmethod
    def remove_expired(cls):
        """Iterates through all approved events and removes those who have a date that has already passed"""
        events = cls.get_approved()
        for event in events:
            event_date = datetime.strptime(event.date, '%Y-%m-%d')
            cur_date = datetime.now()
            if event_date < cur_date:
                event.expire()


