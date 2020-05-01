import uuid
from datetime import datetime
from moviepy.editor import *

#from src.common.database import Database
from common.database import Database


class Trailer(object):

    def __init__(self, author, email, display_email, title, trailer, uploads_dir, link=None, _id=None):
        self.author = author
        self.email = email
        self.display_email = display_email
        self.title = title
        self.link = link
        self._id = uuid.uuid4().hex if _id is None else _id
        self.trailer_path = os.path.join(uploads_dir, self._id)
        trailer.save(self.trailer_path)

    def save_to_mongo(self):
        Database.insert(collection='pending_trailers', data=self.json())

    def approve(self):
        q = { '_id': self._id}
        Database.delete_one(collection='pending_trailers', query=q)
        Database.insert(collection='approved_trailers', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'email': self.email,
            'display_email': self.display_email,
            'title': self.title,
            'trailer': self.trailer_path,
            'link': self.link
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

    @classmethod
    def get_approved(cls):
        posts = Database.find(collection='approved_trailers', query={})
        return [cls(**post) for post in posts]

    @classmethod
    def get_pending(cls):
        posts = Database.find(collection='pending_trailers', query={})
        return [cls(**post) for post in posts]
