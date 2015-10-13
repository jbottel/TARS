import os
import TARS
import unittest
import tempfile
import settings
import flask
from xbmcjson import XBMC, PLAYER_VIDEO

class StatusCodeTestCase(unittest.TestCase):
    """Test the TARS main pages for a proper status code response.

    All of the main pages should respond with a HTTP 200 OK proper response
    and this class tests each to page to ensure that this is the case.
    """

    def setUp(self):
        TARS.app.config['TESTING'] = True
        self.c = TARS.app.test_client()

    def tearDown(self):
        pass

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
    """Test the TARS Remote Control functions against the Kodi player.

    The remote control template has a few very important functions that
    are depended on in multiple areas of the app. We test against the Kodi
    player by using a direct JSON-RPC connection to ensure that the Kodi
    player state matches the expected state after running the TARS remote
    control requests.
    
    """

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

class ApplicationFunctionsTestCase(unittest.TestCase):
    """Test the application functions for Kodi application state.

    This set of tests specifically has to do with configuration
    and options dealing with the Kodi application state. A direct
    JSON-RPC API connection is required to retrieve the current
    state and compare it with the expected application state.
    
    """

    def setUp(self):
        TARS.app.config['TESTING'] = True
        self.xbmc = XBMC(settings.JSONRPC_URI + '/jsonrpc')
        self.c = TARS.app.test_client()

    def tearDown(self):
        pass

    def test_set_volume(self):
        """Check that set_volume() functions changes the Kodi system volume when requested."""

        current_volume = self.xbmc.Application.GetProperties( {"properties": ["volume", "muted"]})["result"]["volume"]

        # First set to an arbitary value (low enough not to blow speakers!)
        self.xbmc.Application.SetVolume({"volume": 2})

        # Send the set_volume() request
        result = self.c.get('/set/volume/1')
        volume_properties = self.xbmc.Application.GetProperties( {"properties": ["volume", "muted"]})["result"]
        self.assertEqual(volume_properties["volume"],1)

        # Return volume to level before the test
        self.xbmc.Application.SetVolume({"volume": current_volume})

class TARSSupportFunctionTestCase(unittest.TestCase):
    """Test the TARS support functions for proper operation. 

    Among the tests, this set of tests is the most traditional, i.e., the 
    idea is to make sure that the functions being tested are robust and 
    will give the correct answer each time. These are functions within TARS
    which format or otherwise process data for other functions so they
    should be well tested.
    """
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_runtime(self):
        """Check that format_runtime functions properly for both runtime styles."""
        result = TARS.format_runtime(0)
        self.assertEqual(result, "0 min 0 sec")

        result = TARS.format_runtime(0,"colon")
        self.assertEqual(result, "0:00")

        result = TARS.format_runtime(60,"colon")
        self.assertEqual(result, "1:00")

        result = TARS.format_runtime(200)
        self.assertEqual(result, "3 min 20 sec")

        result = TARS.format_runtime(200,"colon")
        self.assertEqual(result, "3:20")

        result = TARS.format_runtime(123123)
        self.assertEqual(result, "34 hr 12 min")

        result = TARS.format_runtime(123123,"colon")
        self.assertEqual(result, "34:12:03")

        # Test with float input
        result = TARS.format_runtime(float(60),"colon")
        self.assertEqual(result, "1:00")

        result = TARS.format_runtime(float(200))
        self.assertEqual(result, "3 min 20 sec")

        result = TARS.format_runtime(float(123123))
        self.assertEqual(result, "34 hr 12 min")

        result = TARS.format_runtime(float(123123),"colon")
        self.assertEqual(result, "34:12:03")

if __name__ == '__main__':
    unittest.main()
