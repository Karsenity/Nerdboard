import uuid
from datetime import datetime
from moviepy.editor import *

#from src.common.database import Database
from common.database import Database


class Trailer(object):

    def __init__(self, author, email, display_email, title, trailer_path, link=None, _id=None):
        self.author = author
        self.email = email
        self.display_email = display_email
        self.title = title
        self.trailer_path = trailer_path
        self.link = link
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='pending_trailers', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'email': self.email,
            'display_email': self.display_email,
            'title': self.title,
            'trailer_path': self.trailer_path,
            'link': self.link,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='pending_trailers', query={'_id': id})
        return cls(**post_data)

    @classmethod
    def get_all(cls):
        trailers = Database.find(collection='pending_trailers', query={})
        return [cls(**trailer) for trailer in trailers]

    @classmethod
    def to_gif(cls, video):
        clip = (VideoFileClip(video))
        clip.preview()
        clip.write_gif("use_your_head.gif")
