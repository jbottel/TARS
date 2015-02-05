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
    xbmc.Player.PlayPause({"playerid":0})
    xbmc.Player.PlayPause({"playerid":1})
    return ''

@app.route('/remote/left')
def remote_left():
    xbmc.Input.Left()
    return ''

@app.route('/remote/right')
def remote_right():
    xbmc.Input.Right()
    return ''

@app.route('/remote/up')
def remote_up():
    xbmc.Input.Up()
    return ''

@app.route('/remote/down')
def remote_down():
    xbmc.Input.Down()
    return ''

@app.route('/remote/select')
def remote_select():
    xbmc.Input.Select()
    return ''


if __name__ == '__main__':
    xbmc = XBMC("http://192.168.1.2:8080/jsonrpc")
    app.run(debug=True,host='0.0.0.0')
