from flask import Flask
from flask import render_template
from flask import jsonify
from xbmcjson import XBMC, PLAYER_VIDEO
app = Flask(__name__)
app.config.from_object('settings')

@app.route('/')
def index():
    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(
                {"properties":["showtitle","title","episode","season","firstaired","plot","thumbnail"],"limits":{"end":5}})["result"]["episodes"]
    except:
        recently_added_episodes = []

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(
                {"properties":["originaltitle","year","plot","thumbnail","cast","imdbnumber"],"limits":{"end":5}})["result"]["movies"]
    except:
        recently_added_movies = []

    try:
        video_playlist = xbmc.Playlist.GetItems({"properties":["runtime","showtitle","title"], "playlistid":1})["result"]["items"]
        audio_playlist = xbmc.Playlist.GetItems({"properties":["duration","artist","title"], "playlistid":0})["result"]["items"]
        playlist = video_playlist + audio_playlist
    except:
        playlist = []



#    for episode in recently_added_episode_results:
#        episode_details = xbmc.VideoLibrary.Get
    return render_template('index.html',**locals())

@app.route("/movies")
def movies():
    try:
        recently_added_movies_list = xbmc.VideoLibrary.GetRecentlyAddedMovies(
                {"properties":["originaltitle","year","plot","thumbnail","cast","imdbnumber","trailer"],"limits":{"end":15}})["result"]["movies"]
        recently_added_movies  = [recently_added_movies_list[i:i+3] for i in range(0, len(recently_added_movies_list), 3)]


    except:
        recently_added_movies = []
    return render_template('movies.html',**locals())



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

@app.route('/play/movie/<int:movie_id>')
def play_movie(movie_id):
    xbmc.Playlist.Add({'item':{'movieid': movie_id},'playlistid':1})
    xbmc.Player.Open({'item':{'movieid': movie_id}})
    return ''

@app.route('/enqueue/movie/<int:movie_id>')
def enqueue_movie(episode_id):
    xbmc.Playlist.Add({'item':{'movieid': movie_id},'playlistid':1})
    return ''

@app.route('/play/episode/<int:episode_id>')
def play_episode(episode_id):
    xbmc.Playlist.Add({'item':{'episodeid': episode_id},'playlistid':1})
    xbmc.Player.Open({'item':{'episodeid': episode_id}})
    return ''

@app.route('/enqueue/episode/<int:episode_id>')
def enqueue_episode(episode_id):
    xbmc.Playlist.Add({'item':{'episodeid': episode_id},'playlistid':1})
    return ''

@app.route('/play/trailer/<int:movie_id>')
def play_trailer(movie_id):
    details = xbmc.VideoLibrary.GetMovieDetails({"movieid": movie_id,"properties":["trailer"]})
    trailer = details["result"]["moviedetails"]["trailer"]
    xbmc.Player.Open({'item':{'file': trailer}})
    return ''


def format_runtime(item_runtime):
    """Format a runtime in seconds to a human readable format in hours and minutes"""
    if item_runtime > 3600:
        hours = item_runtime/3600
        minutes = item_runtime/60 - (hours*60)
        if minutes == 0:
            newruntime = str(hours) + " hr "
        else:
            newruntime = str(hours) + " hr " + str(minutes) + " min" 
    else: 
        minutes = item_runtime/60
        newruntime = str(minutes) + " min"

    return newruntime

@app.route('/info/movie/<int:movie_id>')
def info_movie(movie_id):
    props = ["thumbnail","originaltitle","year","runtime","genre",
            "director","cast", "plot","trailer","imdbnumber", "mpaa"]
    details = xbmc.VideoLibrary.GetMovieDetails({"movieid": movie_id,"properties":props})
    movie = details["result"]["moviedetails"]

    # Format MPAA Rating to remove "Rating"
    movie["mpaa"] = movie["mpaa"].replace("Rated","",1)

    # Format the movie runtime into a human readable format
    movie["runtime"] = format_runtime(movie["runtime"])

    return render_template('info-movie.html',**locals())

@app.route('/info/episode/<int:episode_id>')
def info_episode(episode_id):
    props = ["thumbnail","showtitle","title","plot","cast","runtime","season","episode","firstaired"]
    details = xbmc.VideoLibrary.GetEpisodeDetails({"episodeid": episode_id,"properties":props})
    episode = details["result"]["episodedetails"]

    # Format the movie runtime into a human readable format
    episode["runtime"] = format_runtime(episode["runtime"])

    return render_template('info-episode.html',**locals())


@app.route('/get_properties')
def get_properties():
    properties = xbmc.Player.GetProperties({"playerid":1,"properties":["time","percentage","totaltime"]})
    return jsonify(properties)

@app.route('/get_duration')
def get_duration():
    properties = xbmc.Player.GetProperties({"playerid":1,"properties":["totaltime"]})
    return jsonify(properties)


if __name__ == '__main__':
    xbmc = XBMC(app.config["KODI_URI"]+"/jsonrpc")
    app.run(debug=True,host='0.0.0.0')
