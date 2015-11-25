
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api import users

from flask_restful import reqparse, abort, Api, Resource

from ..decorators import login_required, admin_required
from ..models.PaletteModel import PaletteModel
from ..services.PaletteService import PaletteService

# Entry
# shows a single palette item and lets you delete a palette item
class Palette(Resource):
    def get(self, palette_id):

        palette = PaletteModel.get_by_id(int(palette_id))
        if palette is None:
            return {'status' : 404, 'message' : 'palette not found'}, 404

        return PaletteModel.format(palette), 200

    def delete(self, palette_id):
        palette = PaletteModel.get_by_id(int(palette_id))
        if palette is None:
            return {'status' : 404, 'message' : 'palette not found'}, 404
        palette.delete()
        return '', 204

    def put(self, palette_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')

        args = parser.parse_args()
        palette = PaletteModel.get_by_id(int(palette_id))
        if palette is None:
            return {'status' : 404, 'message' : 'palette not found'}, 404

        palette.title = args['title']
        palette.description = args['description']

        try:
            palette.put()
            return PaletteModel.format(palette), 201
        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500




# EntryList
# shows a list of all entries, and lets you POST to add new palette
class PaletteList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cursor')

        args = parser.parse_args()
        curs = Cursor(urlsafe=args['cursor'])

        q = PaletteModel.query()
        q_forward = q.order(-PaletteModel.timestamp)
        q_reverse = q.order(PaletteModel.timestamp)

        entries, next_curs, more = q_forward.fetch_page(10, start_cursor=curs)


        out = []
        for palette in entries:
            out.append(PaletteModel.format(palette))

        nextCurs = ""
        if more:
            nextCurs = next_curs.urlsafe()

        prevCurs = ""
        if next_curs is not None:
            rev_cursor = next_curs.reversed()
            old_entries, prev_cursor, fewer = q_reverse.fetch_page(10, start_cursor=rev_cursor, offset=len(out))
            if prev_cursor is not None:
                prevCurs = prev_cursor.urlsafe()

        return {
            'meta': {
                'prev_curs': prevCurs,
                'curs': curs.urlsafe(), 
                'next_curs': nextCurs
            },
            'entries': out
        }

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image_id')
        parser.add_argument('title')
        parser.add_argument('description')

        args = parser.parse_args()

        colors = PaletteService.getPalette(args['image_id'])
        
        palette = PaletteModel(
            image_id = args['image_id'],
            color_primary = colors['primary'],
            color_secondary = colors['secondary'],
            color_accent = colors['accent'],
            title = args['title'],
            description = args['description'],
            added_by = users.get_current_user()
        )

        try:
            palette.put()
            return PaletteModel.format(palette), 201

        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500
