import os
import TARS
import unittest
import tempfile
import settings
import flask
from xbmcjson import XBMC, PLAYER_VIDEO

class StatusCodeTestCase(unittest.TestCase):

    def setUp(self):
        TARS.app.config['TESTING'] = True
        self.xbmc = XBMC(settings.JSONRPC_URI + '/jsonrpc')
        self.c = TARS.app.test_client()

    def tearDown(self):
        pass

    # Test main pages for proper status code

    def test_home_status_code(self):
        result = self.c.get('/') 
        self.assertEqual(result.status_code, 200) 

    def test_movies_status_code(self):
        result = self.c.get('/movies') 
        self.assertEqual(result.status_code, 200) 

    def test_movies_by_title_status_code(self):
        result = self.c.get('/movies/title')
        self.assertEqual(result.status_code, 200) 

    def test_movies_by_title_info_status_code(self):
        result = self.c.get('/movies/title/info')
        self.assertEqual(result.status_code, 200) 

    def test_movies_by_genre_status_code(self):
        result = self.c.get('/movies/genre')
        self.assertEqual(result.status_code, 200) 

    def test_movies_by_collection_status_code(self):
        result = self.c.get('/movies/set')
        self.assertEqual(result.status_code, 200) 

    def test_tvshow_status_code(self):
        result = self.c.get('/tv-shows') 
        self.assertEqual(result.status_code, 200) 

    def test_search_status_code(self):
        result = self.c.get('/search?query=test')
        self.assertEqual(result.status_code, 200) 

    def test_remote_status_code(self):
        result = self.c.get('/remote')
        self.assertEqual(result.status_code, 200) 

if __name__ == '__main__':
    unittest.main()
