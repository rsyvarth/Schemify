#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

TODO: These tests need to be updated to support the Python 2.7 runtime

"""
import os
import io
import json
import unittest

from google.appengine.ext import testbed

from application import app


class TestCases(unittest.TestCase):
    def setUp(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        # Setups app engine test bed. See: http://code.google.com/appengine/docs/python/tools/localunittesting.html#Introducing_the_Python_Testing_Utilities
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def setCurrentUser(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'


    def uploadImage(self):
        with open ("tests/test.png", "rb") as myfile:
            data=myfile.read()

        self.setCurrentUser(u'john@example.com', u'123')
        rv = self.app.post('/api/images', data = {
            'file': (io.BytesIO(data), 'test.png'),
        })

        return json.loads(rv.data)['id']

    def addPalette(self):
        self.setCurrentUser(u'john@example.com', u'123')
        id = self.uploadImage()

        rv = self.app.post('/api/palettes', data=dict(
            title = 'Test', 
            image_id = id,
            description = ''
        ))

        assert rv.status == '201 CREATED'
        return json.loads(rv.data)

    def addLike(self, palette_id):
        rv = self.app.post('/api/likes', data = {
            'palette_id': palette_id
        })

        return json.loads(rv.data)

    ############################################################
    # PALETTE TESTS
    ############################################################

    def test_empty_palette_list(self):
        rv = self.app.get('/api/palettes')
        assert rv.status == '200 OK'
        assert '{"meta": {"next_curs": "", "curs": "", "prev_curs": ""}, "entries": []}' in rv.data

    def test_add_palette(self):
        resp = self.addPalette()
        assert resp['image_id'] == '1'
        assert resp['title'] == 'Test'

    def test_palette_list(self):
        self.addPalette()
        self.addPalette()
        self.addPalette()

        rv = self.app.get('/api/palettes')
        resp = json.loads(rv.data)

        assert len(resp['entries']) == 3

    def test_palette_paging(self):
        for i in range(0, 15):
            self.addPalette()

        rv = self.app.get('/api/palettes')
        resp = json.loads(rv.data)
        assert len(resp['entries']) == 10

        rv = self.app.get('/api/palettes?cursor='+resp['meta']['next_curs'])
        resp = json.loads(rv.data)

        assert len(resp['entries']) == 5
    
    ############################################################
    # USER TESTS
    ############################################################

    def test_user_self(self):
        self.setCurrentUser(u'john@example.com', u'123')

        rv = self.app.get('/api/users/self')
        resp = json.loads(rv.data)

        assert resp['username'] == 'john@example.com'
        assert resp['user_id'] == '123'

    ############################################################
    # LIKE TESTS
    ############################################################

    def test_empty_like_list(self):
        rv = self.app.get('/api/likes?palette_id=1')
        assert rv.status == '200 OK'
        assert '{"meta": {"next_curs": "", "curs": "", "prev_curs": ""}, "likes": []}' in rv.data

    def test_add_like(self):
        palette = self.addPalette()
        assert palette['like_count'] == 0

        self.setCurrentUser(u'john2@example.com', u'12')
        resp = self.addLike(palette['id'])

        assert int(resp['palette_id']) == int(palette['id'])
        assert resp['added_by']['user_id'] == '12'

        rv = self.app.get('/api/palettes/'+str(palette['id']))
        updatedPalette = json.loads(rv.data)
        assert updatedPalette['like_count'] == 1

    def test_add_likes(self):
        palette = self.addPalette()
        assert palette['like_count'] == 0

        self.setCurrentUser(u'john2@example.com', u'12')
        resp = self.addLike(palette['id'])
        self.setCurrentUser(u'john3@example.com', u'13')
        resp = self.addLike(palette['id'])
        self.setCurrentUser(u'john4@example.com', u'14')
        resp = self.addLike(palette['id'])

        rv = self.app.get('/api/palettes/'+str(palette['id']))
        updatedPalette = json.loads(rv.data)
        assert updatedPalette['like_count'] == 3

    def test_add_multiple_likes(self):
        palette = self.addPalette()
        assert palette['like_count'] == 0

        self.setCurrentUser(u'john2@example.com', u'12')
        resp = self.addLike(palette['id'])
        resp = self.addLike(palette['id'])
        resp = self.addLike(palette['id'])

        rv = self.app.get('/api/palettes/'+str(palette['id']))
        updatedPalette = json.loads(rv.data)
        assert updatedPalette['like_count'] == 1


    def test_remove_likes(self):
        palette = self.addPalette()
        assert palette['like_count'] == 0

        self.setCurrentUser(u'john2@example.com', u'12')
        resp = self.addLike(palette['id'])
        self.setCurrentUser(u'john3@example.com', u'13')
        resp = self.addLike(palette['id'])
        self.setCurrentUser(u'john4@example.com', u'14')
        resp = self.addLike(palette['id'])

        rv = self.app.get('/api/palettes/'+str(palette['id']))
        updatedPalette = json.loads(rv.data)
        assert updatedPalette['like_count'] == 3

        t = self.app.delete('/api/likes?palette_id='+str(palette['id']))

        rv = self.app.get('/api/palettes/'+str(palette['id']))
        updatedPalette = json.loads(rv.data)
        assert updatedPalette['like_count'] == 2


if __name__ == '__main__':
    unittest.main()
