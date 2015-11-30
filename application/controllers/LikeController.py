
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api import users
from google.appengine.ext import ndb

from flask_restful import reqparse, abort, Api, Resource

from ..decorators import login_required, admin_required
from ..models.LikeModel import LikeModel
from ..models.PaletteModel import PaletteModel

# Entry
# shows a single like item and lets you delete a like item
class Like(Resource):
    def get(self, like_id):
        like = LikeModel.get_by_id(int(like_id))
        if like is None:
            return {'status' : 404, 'message' : 'like not found'}, 404

        return LikeModel.format(like), 200


# EntryList
# shows a list of all entries, and lets you POST to add new like
class LikeList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cursor')
        parser.add_argument('palette_id')

        args = parser.parse_args()
        curs = Cursor(urlsafe=args['cursor'])

        if args['palette_id'] is None:
            return {'status' : 404, 'message' : 'palette_id required'}, 404

        q = LikeModel.query(LikeModel.palette_id == args['palette_id'])

        q_forward = q.order(-LikeModel.timestamp)
        q_reverse = q.order(LikeModel.timestamp)

        entries, next_curs, more = q_forward.fetch_page(10, start_cursor=curs)


        out = []
        for like in entries:
            out.append(LikeModel.format(like))

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
            'likes': out
        }

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('palette_id')

        args = parser.parse_args()

        oldLike = LikeModel.query(ndb.AND(
            LikeModel.palette_id == args['palette_id'], 
            LikeModel.added_by == users.get_current_user()
        )).get()

        if oldLike is not None:
            return LikeModel.format(oldLike), 200

        like = LikeModel(
            palette_id = args['palette_id'],
            added_by = users.get_current_user(),
            added_by_id = users.get_current_user().user_id()
        )

        try:
            like.put()
            PaletteModel.like(like.palette_id, True)

            return LikeModel.format(like), 201

        except CapabilityDisabledError:
            return {'status' : 500, 'message' : 'can\'t access database'}, 500


    @login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('palette_id')

        args = parser.parse_args()

        like = LikeModel.query(ndb.AND(
            LikeModel.palette_id == args['palette_id'], 
            LikeModel.added_by == users.get_current_user()
        )).get()

        if like is None:
            return {'status' : 404, 'message' : 'like not found'}, 404

        PaletteModel.like(like.palette_id, False)
        
        like.key.delete()
        return '', 204
