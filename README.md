TARS - A Remote System
======================
TARS is a web-based remote control system for Kodi (formerly known as XBMC). It allows for controlling Kodi in both traditional remote control style (navigating through Kodi's onscreen menu) and web-based browsing/searching of the Kodi media library. 

![Screenshot of TARS](http://jbottel.github.io/TARS/img/front-page-with-remote.png)

[Additional Screenshots](#additional-screenshots)

TARS is different from some other web interfaces for Kodi: its focus is _function_ over form. Some interfaces are very interested in showing off the library: large art and images, for example. These are nice, but when you have a large media library or you know exactly what you want, these approaches sometimes get in the way. TARS is built to be easy, quick, and functional. The idea is to _interfere as little as possible_ but still maintain a measure of helpfulness. 

Planned / Implemented Features:
- [x] Full Remote Control to navigate Kodi's onscreen menu
- [x] Fully browse the Kodi media library including:
  - [x] Movies
  - [x] TV Shows
  - [ ] Music
- [ ] Browse by files / source
- [x] Search items in the Kodi media library
- [x] Perform library maintenance, including:
  - [x] Scan library
  - [x] Clean library
- [x] Quick access to navigation to specific points within the media using a slider
- [x] Quick access to volume control.

Several open source frameworks and projects are used in the development of this project: [Flask](http://flask.pocoo.org/), [python-xbmc](https://github.com/jcsaaddupuy/python-xbmc), [jQuery](http://jquery.com/), [Bootstrap](http://getbootstrap.com/), [bootstrap-slider](https://github.com/seiyria/bootstrap-slider), and more.

Get TARS
--------------
TARS performs quite well for most users, but is still in development (refer to the feature list above). If interested, you are encouraged to begin using TARS and let me know if you encounter any difficulties. Any interested developers are also welcome to join the project.

A recent version of Python 2 and the flask framework are required. It's recommended that you install flask using pip.
```
pip install flask
git clone https://github.com/jbottel/TARS.git
```

How To Run
----------
You'll need to edit `settings.py` to set up your local Kodi JSON-RPC, Kodi Web URI and DEBUG settings.
```
vi/nano/emacs settings.py 
```

You will likely want to keep `DEBUG = True` while TARS is in development. You'll need to set `JSONRPC_URI` to the HTTP address that Kodi is serving up the JSON-RPC API, for example, `JSONRPC_URI = 'http://10.0.0.1:8080'`. You'll also want to set `KODI_URI` to the HTTP address that a client web browser can use to access Kodi's image library via HTTP.

Run TARS
```
python TARS.py
```

TARS is now listening for connections. The default port is 5000.

Enjoy!


Tests
----------
An application like TARS is difficult to test, however, an attempt will be made to provide tests to the level where it is possible -- keep in mind that Kodi itself is not very well tested, however. Because of the nature of TARS, for nearly all tests a direct connection to the JSON-RPC API is required, and thus a Kodi instance must be running. Additionally, the Kodi instance must have some media to test with: at least one movie should exist in the Kodi database with a `movieid` of `1`. Unsurprisingly, any permissions to run TARS as normal are also required for testing. The Kodi player will flash items on and off during the tests. 

After ensuring that the JSON-RPC API is correctly configured in `settings.py` and that your media library meets the specifications, you can run the test suite by running:
```
python tests.py
```

If the attached Kodi library is very large, the tests can take a significant amount of time to run, since several database-wide queries will be executed.


Additional Screenshots
----------
**Movies Page**
![Screenshot of TARS Movies Page](http://jbottel.github.io/TARS/img/movies-page.png)

**TV Page**
![Screenshot of TARS Movies Page](http://jbottel.github.io/TARS/img/tv-page.png)

**Remote and Navigation Slider**

![Screenshot of TARS Movies Page](http://jbottel.github.io/TARS/img/remote.gif)
![Screenshot of TARS Movies Page](http://jbottel.github.io/TARS/img/select.gif)
