

from google.appengine.ext import ndb
from UserModel import UserModel

class PaletteModel(ndb.Model):
    """Palette Model"""
    image_id = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @staticmethod
    def format(palette):
        if palette is None or palette.timestamp is None:
            return {}

        return {
            # 'id': palette.key.urlsafe(),
            'id': palette.key.id(),
            'image_id': palette.image_id,
            'title': palette.title,
            'description': palette.description,
            'added_by': UserModel.format(palette.added_by),
            'timestamp': palette.timestamp.isoformat(),
            'updated': palette.updated.isoformat()
        }