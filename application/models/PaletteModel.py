
from google.appengine.api import users

from google.appengine.ext import ndb
from UserModel import UserModel
from LikeModel import LikeModel

class PaletteModel(ndb.Model):
    """Palette Model"""
    image_id = ndb.StringProperty(required=True)
    color_primary = ndb.StringProperty(required=True)
    color_secondary = ndb.StringProperty(required=True)
    color_accent = ndb.StringProperty(required=True)
    
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=False)
    like_count = ndb.IntegerProperty(default=0)
    
    added_by = ndb.UserProperty()
    added_by_id = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @staticmethod
    def like(palette_id, add):
        palette = PaletteModel.get_by_id(int(palette_id))
        
        if palette is None:
            return False

        if add:
            palette.like_count += 1
        else:
            palette.like_count -= 1

        palette.put()

        return True

    @staticmethod
    def format(palette):
        if palette is None or palette.timestamp is None:
            return {}

        like = LikeModel.query(ndb.AND(
            LikeModel.palette_id == str(palette.key.id()), 
            LikeModel.added_by == users.get_current_user()
        )).get()

        return {
            # 'id': palette.key.urlsafe(),
            'id': palette.key.id(),
            'image_id': palette.image_id,
            'color_primary': palette.color_primary,
            'color_secondary': palette.color_secondary,
            'color_accent': palette.color_accent,

            'user_like': LikeModel.format(like),
            
            'title': palette.title,
            'description': palette.description,
            'like_count': palette.like_count,
            'added_by': UserModel.format(palette.added_by),
            'timestamp': palette.timestamp.isoformat(),
            'updated': palette.updated.isoformat()
        }