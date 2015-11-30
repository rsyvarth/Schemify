"""
routes.py

URL dispatch route mappings and error handlers

"""

from flask import render_template
from flask.ext.cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from application import app

from controllers.AuthController import login, logout
from controllers.PaletteController import Palette, PaletteList
from controllers.ImageController import Image, ImageList
from controllers.LikeController import Like, LikeList
from controllers.UserController import UserSelf

# Allow cross domain requests from localhost 
CORS(app, resources={r"/api/*": {"origins": "http://localhost:1234"}})

# API Endpoints
api = Api(app)
api.add_resource(UserSelf, '/api/users/self')

api.add_resource(PaletteList, '/api/palettes')
api.add_resource(Palette, '/api/palettes/<palette_id>')

api.add_resource(ImageList, '/api/images')
api.add_resource(Image, '/api/images/<image_id>')

api.add_resource(LikeList, '/api/likes')
api.add_resource(Like, '/api/likes/<like_id>')

# Login page
app.add_url_rule('/login', 'login', view_func=login)
app.add_url_rule('/logout', 'logout', view_func=logout)

## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
app.add_url_rule('/api/_ah/warmup', 'warmup', view_func=warmup)
