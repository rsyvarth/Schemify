
from google.appengine.ext import ndb, db
from UserModel import UserModel

from flask import Response

class ImageModel(ndb.Model):
    """Image Model"""
    image = ndb.BlobProperty()
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def setImage(self, filestream):
        self.image = db.Blob(filestream)
    
    @staticmethod
    def displayImage(image):
        resp = Response(image.image, mimetype='image/png')
        resp.status_code = 200

        return resp;
    
    @staticmethod
    def format(image):
        if image is None:
            return {}

        return {
            'id': image.key.id(),
            'added_by': UserModel.format(image.added_by),
            'timestamp': image.timestamp.isoformat()
        }

