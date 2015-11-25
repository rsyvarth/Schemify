

from google.appengine.ext import ndb
from UserModel import UserModel

class PaletteModel(ndb.Model):
    """Palette Model"""
    image_id = ndb.StringProperty(required=True)
    color_primary = ndb.StringProperty(required=True)
    color_secondary = ndb.StringProperty(required=True)
    color_accent = ndb.StringProperty(required=True)
    
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
            'color_primary': palette.color_primary,
            'color_secondary': palette.color_secondary,
            'color_accent': palette.color_accent,
            
            'title': palette.title,
            'description': palette.description,
            'added_by': UserModel.format(palette.added_by),
            'timestamp': palette.timestamp.isoformat(),
            'updated': palette.updated.isoformat()
        }