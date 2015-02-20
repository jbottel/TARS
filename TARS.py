from flask import Flask
from flask import render_template
from xbmcjson import XBMC, PLAYER_VIDEO
app = Flask(__name__)

@app.route('/')
def index():
    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(
                {"properties":["showtitle","title","episode","season","firstaired","plot","thumbnail"],"limits":{"end":5}})["result"]["episodes"]
    except:
        recently_added_episodes = []

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(
                {"properties":["originaltitle","year","plot","thumbnail","cast"],"limits":{"end":5}})["result"]["movies"]
    except:
        recently_added_movies = []



#    for episode in recently_added_episode_results:
#        episode_details = xbmc.VideoLibrary.Get
    return render_template('index.html',**locals())

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
    #if are_players_active():
    #    xbmc.Player.seek({"value":"smallbackward","playerid":1})
    return ''

@app.route('/remote/right')
def remote_right():
    xbmc.Input.Right()
    #if are_players_active():
    #    xbmc.Player.seek({"value":"smallforward","playerid":1})
    return ''

@app.route('/remote/up')
def remote_up():
    xbmc.Input.Up()
    #if are_players_active():
    #    xbmc.Player.seek({"value":"bigforward","playerid":1})
    return ''

@app.route('/remote/down')
def remote_down():
    xbmc.Input.Down()
    #if are_players_active():
    #    xbmc.Player.seek({"value":"bigbackward","playerid":1})
    return ''

@app.route('/remote/select')
def remote_select():
    xbmc.Input.Select()
    return 

@app.route('/remote/rewind')
def remote_rewind():
    xbmc.Input.ExecuteAction({"action":"analogrewind"})
    return ''

@app.route('/remote/fastforward')
def remote_fastforward():
    xbmc.Input.ExecuteAction({"action":"analogfastforward"})
    return ''

@app.route('/remote/previous')
def remote_previous():
    xbmc.Player.GoTo({"to":"previous", "playerid":1})
    return ''

@app.route('/remote/next')
def remote_next():
    xbmc.Player.GoTo({"to":"next", "playerid":1})
    return ''


@app.route('/remote/stop')
def remote_stop():
    xbmc.Player.Stop({"playerid":1})
    return ''

@app.route('/remote/title')
def remote_title():
    xbmc.Input.ContextMenu()
    return ''

@app.route('/remote/info')
def remote_info():
    xbmc.Input.Info()
    return ''

@app.route('/remote/menu')
def remote_menu():
    xbmc.Input.ShowOSD()
    return ''

@app.route('/remote/back')
def remote_back():
    xbmc.Input.Back()
    return ''


@app.route('/remote/players')
def remote_players():
    if are_players_active():
        return 'yah'
    else:
        return 'nah'

def are_players_active():
    if xbmc.Player.GetActivePlayers()["result"]:
        return True

if __name__ == '__main__':
    xbmc = XBMC("http://localhost:8080/jsonrpc")
    app.run(debug=True,host='0.0.0.0')
