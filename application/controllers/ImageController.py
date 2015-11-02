
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api import users

from flask import request

from flask_restful import reqparse, abort, Api, Resource

from ..decorators import login_required, admin_required
from ..models.ImageModel import ImageModel

# ImageList
# handles image creation and in theory listing but that isn't supported atm
class ImageList(Resource):

    @login_required
    def post(self):

        file = request.files['file']

        if not file:
            return {'status' : 400, 'message' : 'missing required param: file'}, 400

        filestream = file.read()

        if len(filestream) > 1024*1024:
            return {'status' : 400, 'message' : 'image too large, must be less than 1MB'}, 400

        image = ImageModel()
        image.setImage(filestream)
        image.added_by = users.get_current_user()
        
        try:
            image.put()
            return ImageModel.format(image), 201

        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500


# Image
# shows a single image
class Image(Resource):
    def get(self, image_id):

        image = ImageModel.get_by_id(int(image_id))
        if image is None:
            return {'status' : 404, 'message' : 'image not found'}, 404

        return ImageModel.displayImage(image)

