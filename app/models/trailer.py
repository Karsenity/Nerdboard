import uuid
from datetime import datetime
from moviepy.editor import *

#from src.common.database import Database
from common.database import Database


class Trailer(object):

    def __init__(self, author, email, aoc, title, description, picture=None, _id=None):
        self.author = author
        self.email = email
        self.aoc = aoc
        self.title = title
        self.description = description
        self.picture = picture
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='pending_trailers',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'email': self.email,
            'aoc': self.aoc,
            'title': self.title,
            'description': self.description,
            'picture': self.picture,
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='pending_trailers', query={'_id': id})
        return cls(**post_data)

    @classmethod
    def to_gif(cls, video):
        clip = (VideoFileClip(video))
        clip.preview()
        clip.write_gif("use_your_head.gif")