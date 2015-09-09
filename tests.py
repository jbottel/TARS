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

class RemoteControlTestCase(unittest.TestCase):

    def setUp(self):
        TARS.app.config['TESTING'] = True
        self.xbmc = XBMC(settings.JSONRPC_URI + '/jsonrpc')
        self.c = TARS.app.test_client()

    def tearDown(self):
        pass

    def test_playpause(self):
        """Check that the play/pause functionality properly pauses and playes the Kodi player when requested."""
        # Play the first movie available in the database (will fail if movie database is empty)
        self.xbmc.Player.Open({'item': {'movieid': 1}})

        # Remote Control: Pause
        result = self.c.get('/remote/playpause')
        # Check 'speed' attribute to check
        player_properties = self.xbmc.Player.GetProperties({"playerid": 1, "properties": ["speed"]})["result"] 
        self.assertEqual(player_properties['speed'], 0) 

        # Remote Control: Play
        result = self.c.get('/remote/playpause')
        # Check 'speed' attribute to check
        player_properties = self.xbmc.Player.GetProperties({"playerid": 1, "properties": ["speed"]})["result"] 
        self.assertEqual(player_properties['speed'], 1) 

        self.xbmc.Player.Stop({"playerid": 1})

    def test_stop(self):
        """Check that the stop functionality properly stops the Kodi player when requested."""
        # Play the first movie available in the database (will fail if movie database is empty)
        self.xbmc.Player.Open({'item': {'movieid': 1}})

        # Send stop request
        result = self.c.get('/remote/stop')
        
        # Check active player
        active = self.xbmc.Player.GetActivePlayers()["result"]
        self.assertFalse(active) 

    def test_fast_forward(self):
        """Check that the fast forward functionality properly fast-forwards the Kodi player when requested."""
        # Play the first movie available in the database (will fail if movie database is empty)
        self.xbmc.Player.Open({'item': {'movieid': 1}})

        # Send fast forward request
        result = self.c.get('/remote/fastforward')

        # Check 'speed' attribute to check
        player_properties = self.xbmc.Player.GetProperties({"playerid": 1, "properties": ["speed"]})["result"] 
        
        self.assertEqual(player_properties['speed'], 1) 

        self.xbmc.Player.Stop({"playerid": 1})

if __name__ == '__main__':
    unittest.main()
