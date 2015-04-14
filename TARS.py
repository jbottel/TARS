from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
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
        video_playlist_result = xbmc.Playlist.GetItems({"properties":["runtime","showtitle","title"], "playlistid":1})
        video_playlist = video_playlist_result["result"]["items"]
    except:
        video_playlist = []

    try:
        audio_playlist_result = xbmc.Playlist.GetItems({"properties":["duration","artist","title"], "playlistid":0})
        audio_playlist = audio_playlist_result["result"]["items"]
    except:
        audio_playlist = []

    for item in video_playlist:
        try:
            item["runtime"] = format_runtime(item["runtime"],"colon")
        except:
            item["runtime"] = "Unknown"
        

    for item in audio_playlist:
        try:
            item["duration"] = format_runtime(item["duration"],"colon")
        except:
            item["duration"] = "Unknown"

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


@app.route("/movies/title")
def movies_by_title():
    try:
        movies = xbmc.VideoLibrary.GetMovies(
                {"properties":["originaltitle","year","plot","thumbnail","cast","imdbnumber","trailer"],"sort":{"order":"ascending","method":"title"}})["result"]["movies"]
    except:
        movies = []

    return render_template('movies-by-title.html',**locals())

@app.route("/movies/title/info")
def movies_by_title_info():
    try:
        movies_list = xbmc.VideoLibrary.GetMovies(
                {"properties":["originaltitle","year","plot","thumbnail","cast","imdbnumber","trailer"],"sort":{"order":"ascending","method":"title"}})["result"]["movies"]
        movies  = [movies_list[i:i+3] for i in range(0, len(movies_list), 3)]
    except:
        movies = []

    return render_template('movies-by-title-info.html',**locals())

@app.route("/movies/genre")
def movies_by_genre():
    try:
        genres = xbmc.VideoLibrary.GetGenres({"type":"movie","sort":{"order":"ascending","method":"label"}})
        genres = genres["result"]["genres"]
    except:
        genres = []
    return render_template('movies-by-genre.html',**locals())

@app.route("/movies/genre/<int:genre_id>")
def get_movies_by_genre(genre_id):
    try:
        genres = xbmc.VideoLibrary.GetGenres({"type":"movie","sort":{"order":"ascending","method":"label"}})
        genres = genres["result"]["genres"]

        # Get label for current genre
        for genre in genres:
            if genre["genreid"] == genre_id: 
                this_genre=genre["label"]

        props = ["originaltitle","year","plot","thumbnail","cast","imdbnumber","trailer","genre"]
        movies = xbmc.VideoLibrary.GetMovies({"properties":props,"filter":{"genreid":genre_id}})
        movies = movies["result"]["movies"]
    except:
        genres = []
    return render_template('movies-by-genre.html',**locals())

@app.route("/movies/set")
def movies_by_set():
    try:
        sets_list = xbmc.VideoLibrary.GetMovieSets({"sort":{"order":"ascending","method":"label"}})
        sets = sets_list["result"]["sets"]
    except:
        sets = []
    details = {"result":{"setdetails":{"movies":[]}}}
    return render_template('movies-by-collection.html',**locals())

@app.route("/movies/set/<int:set_id>")
def get_movies_by_set(set_id):
    try:
        sets_list = xbmc.VideoLibrary.GetMovieSets({"sort":{"order":"ascending","method":"label"}})
        sets = sets_list["result"]["sets"]
    except:
        sets = []
    try:
        details = xbmc.VideoLibrary.GetMovieSetDetails({"setid":set_id,"properties":["title","thumbnail"]})
    except:
        details = []

    return render_template('movies-by-collection.html',**locals())



@app.route("/tv-shows")
def tv_shows():
    try:
        recently_added_episodes_list = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(
                {"properties":["showtitle","title","episode","season","firstaired","plot","thumbnail"],"limits":{"end":15}})["result"]["episodes"]
        recently_added_episodes  = [recently_added_episodes_list[i:i+3] for i in range(0, len(recently_added_episodes_list), 3)]
    except:
        recently_added_episodes = []

    try:
        tv_shows_list = xbmc.VideoLibrary.GetTVShows({"sort":{"order":"ascending","method":"title"},"properties":["title","year"]})
        tv_shows = tv_shows_list["result"]["tvshows"]
    except:
        tv_shows = []
    return render_template('tv-shows.html',**locals())

@app.route("/tv-shows/<int:show_id>")
def tv_show_seasons(show_id):

    try:
        show = xbmc.VideoLibrary.GetTVShowDetails({"tvshowid":show_id})["result"]["tvshowdetails"]
    except:
        show = {}

    try:
        episodes_list = xbmc.VideoLibrary.GetEpisodes({"tvshowid":show_id,"sort":{"order":"descending","method":"year"},"limits":{"end":15},"properties":["thumbnail","title","showtitle","season","episode","firstaired"]})
        episodes_result = episodes_list["result"]["episodes"]
        episodes  = [episodes_result[i:i+3] for i in range(0, len(episodes_result), 3)]
    except:
        episodes = []

    try:
        seasons = xbmc.VideoLibrary.GetSeasons({"tvshowid":show_id,"properties":["season"]})
        seasons = seasons["result"]["seasons"]
    except:
        seasons = []
    return render_template('tv-show.html',**locals())

@app.route("/tv-shows/<int:show_id>/<int:season_id>")
def tv_show_seasons_episodes(show_id,season_id):

    try:
        show = xbmc.VideoLibrary.GetTVShowDetails({"tvshowid":show_id})["result"]["tvshowdetails"]
    except:
        show = {}
    try:
        seasons = xbmc.VideoLibrary.GetSeasons({"tvshowid":show_id,"properties":["season"]})
        seasons = seasons["result"]["seasons"]
    except:
        seasons = []

    try:
        episodes_list = xbmc.VideoLibrary.GetEpisodes({"tvshowid":show_id,"season": season_id, "sort":{"order":"ascending","method":"episode"},"properties":["thumbnail","title","showtitle","season","episode","firstaired"]})
        episodes_result = episodes_list["result"]["episodes"]
        episodes  = [episodes_result[i:i+3] for i in range(0, len(episodes_result), 3)]
    except:
        episodes = []

    return render_template('tv-show-episodes.html',**locals())




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

@app.route('/seek/<int:seek_value>')
def seek_player(seek_value):
    seek_value = seek_value * 5
    hours = seek_value / 3600
    minutes = (seek_value - (hours*3600))/60
    seconds = seek_value - hours*3600 - minutes*60
    position = { 'hours': hours, 'minutes': minutes, 'seconds': seconds }
    print xbmc.Player.Seek({'playerid':1,'value':position})
    return ''

@app.route('/set/volume/<int:volume_value>')
def set_volume(volume_value):
    print xbmc.Application.SetVolume({"volume":volume_value})
    return ''

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


def format_runtime(item_runtime, format="text"):
    """Format a runtime in seconds to a human readable format in hours and minutes
    
    Takes a "format" argument that specifies whether the function should return:
    "text" -- "2 hr 7 min"
    "colon" -- "2:07:00"

    """
    if format == "text":
        if item_runtime > 3600:
            hours = item_runtime/3600
            minutes = item_runtime/60 - (hours*60)
            if minutes == 0:
                newruntime = str(hours) + " hr "
            else:
                newruntime = str(hours) + " hr " + str(minutes) + " min" 
        else: 
            minutes = item_runtime/60
            seconds = item_runtime - minutes*60
            newruntime = str(minutes) + " min "+ str(seconds) + " sec"
    if format == "colon":
        if item_runtime > 3600:
            hours = item_runtime/3600
            minutes = item_runtime/60 - (hours*60)
            seconds = item_runtime - minutes * 60 - hours * 3600
            newruntime = str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        else: 
            minutes = item_runtime/60
            seconds = item_runtime - minutes*60
            newruntime = str(minutes) + ":" + str(seconds).zfill(2)

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
    try:
        player_properties = xbmc.Player.GetProperties({"playerid":1,"properties":["time","percentage","totaltime","speed"]})["result"]
        app_properties = xbmc.Application.GetProperties({"properties":["volume","muted"]})["result"]
        playing_properties = xbmc.Player.GetItem({"playerid":1,"properties":["title","season","episode","showtitle","thumbnail"]})["result"]
        properties = dict(player_properties.items() + app_properties.items() + playing_properties.items())
    except:
        properties = {"error":True}
    return jsonify(properties)

@app.route('/get_duration')
def get_duration():
    properties = xbmc.Player.GetProperties({"playerid":1,"properties":["totaltime"]})
    return jsonify(properties)

def get_all_movie_titles():
    movies = xbmc.VideoLibrary.GetMovies(
            {"properties":["originaltitle"],"sort":{"order":"ascending","method":"title"}})["result"]["movies"]
    return movies

def get_all_tv_show_titles():
    tv_shows = xbmc.VideoLibrary.GetTVShows({"properties":["title"],"sort":{"order":"ascending","method":"title"}})["result"]["tvshows"]
    return tv_shows


@app.route('/debug/search_movies/<search_term>')
def debug_search_movies(search_term):
    return jsonify({'movies':search_movies(search_term)})

@app.route('/debug/search_tv/<search_term>')
def debug_search_tv(search_term):
    return jsonify({'tv_shows':search_tv_shows(search_term)})

def search_movies(search_term):
    movies = get_all_movie_titles()
    matching_movies = []
    for movie in movies:
        if search_term.lower() in movie["originaltitle"].lower():
            matching_movies.append(movie)
    return matching_movies

def search_tv_shows(search_term):
    tv_shows = get_all_tv_show_titles()
    matching_tv_shows = []
    for show in tv_shows:
        if search_term.lower() in show["title"].lower():
            matching_tv_shows.append(show)
    return matching_tv_shows

@app.route('/search')
def search_results():
    search_term = request.args.get('query')
    movie_ids = search_movies(search_term)
    tv_show_ids = search_tv_shows(search_term)
    movies = []
    tv_shows = []
    for movie in movie_ids:
        movie_details = xbmc.VideoLibrary.GetMovieDetails({"movieid":movie["movieid"],"properties":["originaltitle","year","plot","thumbnail","cast","imdbnumber","trailer"]})["result"]["moviedetails"]
        movies.append(movie_details)

    for tv_show in tv_show_ids:
        seasons = xbmc.VideoLibrary.GetSeasons({"tvshowid":tv_show["tvshowid"],"properties":["season"]})["result"]
        tv_shows.append({"show":tv_show,"seasons":seasons})
    return render_template('search-results.html',**locals())

if __name__ == '__main__':
    xbmc = XBMC(app.config["KODI_URI"]+"/jsonrpc")
    app.run(debug=True,host='0.0.0.0')
