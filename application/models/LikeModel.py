

from google.appengine.ext import ndb
from UserModel import UserModel

class LikeModel(ndb.Model):
    """Like Model"""
    palette_id = ndb.StringProperty(required=True)
    added_by = ndb.UserProperty()
    added_by_id = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def format(like):
        if like is None or like.timestamp is None:
            return {}

        return {
            'id': like.key.id(),
            'palette_id': like.palette_id,
            'added_by': UserModel.format(like.added_by),
            'timestamp': like.timestamp.isoformat()
        }