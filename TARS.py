from flask import Flask
from flask import render_template
from xbmcjson import XBMC, PLAYER_VIDEO
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remote')
def remote():
    return render_template('remote.html')

@app.route('/remote/playpause')
def remote_playpause():
    xbmc.Player.PlayPause([PLAYER_VIDEO])


if __name__ == '__main__':
    xbmc = XBMC("http://192.168.1.2:8080/jsonrpc")
    app.run(debug=True,host='0.0.0.0')
