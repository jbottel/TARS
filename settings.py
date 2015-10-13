# REQUIRED SETTINGS
# ------------------------------------------------------------------------------------
# These settings must be configured in order for TARS to function properly.
# ------------------------------------------------------------------------------------

# Keep set to "True" while TARS is in development unless the DEBUG messages will 
# mean nothing to you, or you are concerned about resource usage.
DEBUG = True

# Kodi JSON-RPC Server URI
# This is the URL which TARS should contact Kodi's JSON-RPC server
# Do not include /jsonrpc/ on this URL
JSONRPC_URI = 'http://localhost:8080'

# Kodi Image Server URI
# This is the URL which a browser should request from retrieve Kodi's image files.
# In many cases, this should be the same as JSONRPC_URI.
KODI_URI = 'http://localhost:8080'




# ADDITIONAL CUSTOMIZATION SETTINGS
# ------------------------------------------------------------------------------------
# The following are settings which can be modified to change aspects of TARS' behavior.
# Some of these settings are not fully implemented and are here for development
# reference.
# ------------------------------------------------------------------------------------

# Attempt to resume any video that is to be played by checking Kodi's database for a previous
# playtime, and presenting the option of resuming at that time.
ATTEMPT_RESUME_VIDEOS = False

# The number of characters to be used in a description in the "Media Info" view before truncation.
DESCRIPTION_CHAR_LIMIT = 19

# Display the image banner in the Kodi library for the TV Show
DISPLAY_TV_IMAGE_BANNER = True

# Only find results that match the search terms exactly.
EXACT_SEARCH = False

# Rather than display the season number and episode number, instead display the 
# "Aired On" date as reported by Kodi in the now playing information.
PREFER_DATE_OVER_EP_FORMAT = False

# On a TV show main page, should TARS display episodes sequentially starting from the first,
# or should TARS display episodes starting with the most recently added?
PREFER_SEQ_OVER_RECENT = False

# Should the search function match words in the episode descriptions?
SEARCH_IN_EPISODE_DESC = False

# Should the search function match words in movie descriptions?
SEARCH_IN_MOVIE_DESC = False

# Should TARS show the "Clean Library" button on the movies page?
SHOW_CLEAN_LIBRARY_BUTTON = True

# Should TARS display the "IMDB" button on movies?
SHOW_IMDB_BUTTON = True

# Should TARS display playlists on the front page?
SHOW_PLAYLISTS = True

# Should TARS show the "Random Movie" button on the movies page?
SHOW_RANDOM_MOVIE = False

# Should TARS show the "Clean Library" button on the movies page?
SHOW_SCAN_LIBRARY_BUTTON = True

# Should TARS show the "Trailer" button on the movies page?
# Could be used when the Kodi installation is not connected to the Internet
SHOW_TRAILER_BUTTON = True

# How often, in seconds, should TARS update the slider and playback information?
# Keep low for a responsive "Now Playing" bar, or keep high to prevent
# resource usage and network congestion.
SLIDER_REFRESH_INTERVAL = 2

# Should TARS assume that it can control the volume for the system
# by adjusting the in-application Kodi volume settings?
USE_KODI_VOLUME_CONTROL = True

# Should the remote buttons have a different function when media is
# playing wherein the buttons are used to navigate and skip through media files?
USE_REMOTE_FOR_SKIPPING = False
