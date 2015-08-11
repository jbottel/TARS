TARS - A Remote System
======================
TARS is a web-based remote control system for Kodi (formerly known as XBMC). It allows for controlling Kodi in both traditional remote control style (navigating through Kodi's onscreen menu) and web-based browsing/searching of the Kodi media library. 

TARS is different from some other web interfaces for Kodi: its focus is _function_ over form. Some interfaces are very interested in showing off the library: large art and images, for example. These are nice, but when you have a large media library or you know exactly what you want, these approaches sometimes get in the way. TARS is built to be easy, quick, and functional. The idea is to _interfere as little as possible_ but still maintain a measure of helpfulness. In the end, we let the player itself does the showing off, not the remote.

Planned / Implemented Features:
- Full Remote Control to navigate Kodi's onscreen menu
- Fully browse the Kodi media library including:
  - Movies
  - TV Shows
  - Music
- Search items in the Kodi media library
- Perform library maintenance, including:
  - Scan library
  - Clean library
- Quick access to navigation to specific points within the media using a slider
- Quick access to volume control.

Keep in mind that some of these features are not fully implemented as TARS is still in its early development.

Several open source frameworks and projects are used in the development of this project: [Flask](http://flask.pocoo.org/), [python-xbmc](https://github.com/jcsaaddupuy/python-xbmc), [jQuery](http://jquery.com/), [Bootstrap](http://getbootstrap.com/), [bootstrap-slider](https://github.com/seiyria/bootstrap-slider), and more.

Get TARS
--------------
TARS is still under development and likely does not yet provide all the features you might expect in such a project. If you are interested, however, you are very welcome to clone/watch the repository. Interested developers are also welcome.

A recent version of Python 2 and the flask framework are required. It's recommended that you install flask using pip.
```
pip install flask
git clone https://github.com/jbottel/TARS.git
```

How To Run
----------
You'll need to edit `settings.py` to set up your local Kodi URI and DEBUG settings.
```
vi/nano/emacs settings.py 
```

You will likely want to keep `DEBUG = True` while TARS is in development. You'll need to set `JSONRPC_URI` to the HTTP address that Kodi is serving up the JSON-RPC API, for example, `JSONRPC_URI = 'http://10.0.0.1:8080'`. You'll also want to set `KODI_URI` to the HTTP address that a client web browser can use to access Kodi's image library via HTTP.

Run TARS
```
python TARS.py
```

TARS is now listening for connections. The default port is 5000.
