
from google.appengine.api import users
from google.appengine.ext import ndb

class UserModel(ndb.Model):
    """User Model"""
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @staticmethod
    def getSelf():
        return UserModel.format(users.get_current_user())

    @staticmethod
    def format(user):
        if user is None:
            return {}

        return {
            # 'email': user.email(),
            'username': user.nickname(),
            'user_id': user.user_id(),
            'subscribed': False
        }

