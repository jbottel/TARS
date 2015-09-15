from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
import random
from xbmcjson import XBMC, PLAYER_VIDEO
app = Flask(__name__)
app.config.from_object('settings')
xbmc = XBMC(app.config["JSONRPC_URI"] + "/jsonrpc")


@app.route('/')
def index():
    """Compile all of the items necessary on the front page, including:
    - List of recently added episodes
    - List of recently added movies
    - Lists of the video and audio playlist items

    Return a rendered template.
    """

    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(
            {"properties": ["showtitle", "title", "episode", "season", "firstaired", "plot", "thumbnail"], "limits": {"end": 5}})["result"]["episodes"]
    except:
        recently_added_episodes = []

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(
            {"properties": ["originaltitle", "year", "plot", "thumbnail", "cast", "imdbnumber"], "limits": {"end": 5}})["result"]["movies"]
    except:
        recently_added_movies = []

    try:
        video_playlist_result = xbmc.Playlist.GetItems(
            {"properties": ["runtime", "showtitle", "title"], "playlistid": 1})
        video_playlist = video_playlist_result["result"]["items"]
    except:
        video_playlist = []

    try:
        audio_playlist_result = xbmc.Playlist.GetItems(
            {"properties": ["duration", "artist", "title"], "playlistid": 0})
        audio_playlist = audio_playlist_result["result"]["items"]
    except:
        audio_playlist = []

    for item in video_playlist:
        try:
            item["runtime"] = format_runtime(item["runtime"], "colon")
        except:
            item["runtime"] = "Unknown"

    for item in audio_playlist:
        try:
            item["duration"] = format_runtime(item["duration"], "colon")
        except:
            item["duration"] = "Unknown"

    return render_template('index.html', **locals())


@app.route("/movies")
def movies():
    """Compile all of the items necessary on the movies front page, including:
    - Recently added movies

    Return a rendered template.
    """
    try:
        recently_added_movies_list = xbmc.VideoLibrary.GetRecentlyAddedMovies(
            {"properties": ["originaltitle", "year", "plot", "thumbnail", "cast", "imdbnumber", "trailer"], "limits": {"end": 15}})["result"]["movies"]
        recently_added_movies = [recently_added_movies_list[i:i + 3] for i in range(0, len(recently_added_movies_list), 3)]
    except:
        recently_added_movies = []

    return render_template('movies.html', **locals())


@app.route("/movies/title")
def movies_by_title():
    """Compile all of the items necessary on the movies title listing page.

    Return a rendered template.
    """
    try:
        movies = xbmc.VideoLibrary.GetMovies(
            {"properties": ["originaltitle", "year", "plot", "thumbnail", "cast", "imdbnumber", "trailer"], "sort": {"order": "ascending", "method": "title"}})["result"]["movies"]
    except:
        movies = []

    return render_template('movies-by-title.html', **locals())


@app.route("/movies/title/info")
def movies_by_title_info():
    """Compile all of the items necessary on the movies title media info page.

    Return a rendered template.
    """
    try:
        movies_list = xbmc.VideoLibrary.GetMovies(
            {"properties": ["originaltitle", "year", "plot", "thumbnail", "cast", "imdbnumber", "trailer"], "sort": {"order": "ascending", "method": "title"}})["result"]["movies"]
        movies = [movies_list[i:i + 3] for i in range(0, len(movies_list), 3)]
    except:
        movies = []

    return render_template('movies-by-title-info.html', **locals())


@app.route("/movies/genre")
def movies_by_genre():
    """Compile all of the items necessary on the movies by genre listing page.

    Return a rendered template.
    """
    try:
        genres = xbmc.VideoLibrary.GetGenres(
            {"type": "movie", "sort": {"order": "ascending", "method": "label"}})
        genres = genres["result"]["genres"]
    except:
        genres = []
    return render_template('movies-by-genre.html', **locals())


@app.route("/movies/genre/<int:genre_id>")
def get_movies_by_genre(genre_id):
    """Compile all of the items necessary to show movies based on a selected genre, including:
    - List of genres
    - List of movies matching the selected genre

    Return a rendered template.
    """
    try:
        genres = xbmc.VideoLibrary.GetGenres(
            {"type": "movie", "sort": {"order": "ascending", "method": "label"}})
        genres = genres["result"]["genres"]

        # Get label for current genre
        for genre in genres:
            if genre["genreid"] == genre_id:
                this_genre = genre["label"]

        props = ["originaltitle", "year", "plot", "thumbnail",
                 "cast", "imdbnumber", "trailer", "genre"]
        movies = xbmc.VideoLibrary.GetMovies(
            {"properties": props, "filter": {"genreid": genre_id}})
        movies = movies["result"]["movies"]
    except:
        genres = []
    return render_template('movies-by-genre.html', **locals())


@app.route("/movies/set")
def movies_by_set():
    """Compile all of the items necessary to show movies by set/collection listing page.
    - List of sets/collections

    Return a rendered template.
    """
    try:
        sets_list = xbmc.VideoLibrary.GetMovieSets(
            {"sort": {"order": "ascending", "method": "label"}})
        sets = sets_list["result"]["sets"]
    except:
        sets = []
    details = {"result": {"setdetails": {"movies": []}}}
    return render_template('movies-by-collection.html', **locals())


@app.route("/movies/set/<int:set_id>")
def get_movies_by_set(set_id):
    """Compile all of the items necessary to show movies based on a selected set/collection, including:
    - List of sets/collections
    - List of movies matching the selected set

    Return a rendered template.
    """
    try:
        sets_list = xbmc.VideoLibrary.GetMovieSets(
            {"sort": {"order": "ascending", "method": "label"}})
        sets = sets_list["result"]["sets"]
    except:
        sets = []
    try:
        details = xbmc.VideoLibrary.GetMovieSetDetails(
            {"setid": set_id, "properties": ["title", "thumbnail"]})
    except:
        details = []

    return render_template('movies-by-collection.html', **locals())


@app.route("/tv-shows")
def tv_shows():
    """Compile all of the items necessary to generate the TV show main page, including:
    - List of recently added episodes
    - List of all TV shows 

    Return a rendered template.
    """
    try:
        recently_added_episodes_list = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(
            {"properties": ["showtitle", "title", "episode", "season", "firstaired", "plot", "thumbnail","playcount"], "limits": {"end": 15}})["result"]["episodes"]
        recently_added_episodes = [recently_added_episodes_list[
            i:i + 3] for i in range(0, len(recently_added_episodes_list), 3)]
    except:
        recently_added_episodes = []

    try:
        tv_shows_list = xbmc.VideoLibrary.GetTVShows(
            {"sort": {"order": "ascending", "method": "title"}, "properties": ["title", "year"]})
        tv_shows = tv_shows_list["result"]["tvshows"]
    except:
        tv_shows = []

    return render_template('tv-shows.html', **locals())


@app.route("/tv-shows/<int:show_id>")
def tv_show_seasons(show_id):
    """Compile all of the items necessary to show seasons for a selected TV show, including:
    - List of recent episodes 
    - List of seasons matching the TV Show
    - Dictionary of TV show details

    Return a rendered template.
    """
    try:
        show = xbmc.VideoLibrary.GetTVShowDetails(
                {"tvshowid": show_id, "properties": ["plot", "art"]})["result"]["tvshowdetails"]
    except:
        show = {}

    try:
        episodes_list = xbmc.VideoLibrary.GetEpisodes({"tvshowid": show_id, "sort": {"order": "descending", "method": "year"}, "limits": {
                                                      "end": 15}, "properties": ["thumbnail", "title", "showtitle", "season", "episode", "firstaired","playcount"]})
        episodes_result = episodes_list["result"]["episodes"]
        episodes = [episodes_result[i:i + 3]
                    for i in range(0, len(episodes_result), 3)]
    except:
        episodes = []

    try:
        seasons = xbmc.VideoLibrary.GetSeasons(
            {"tvshowid": show_id, "properties": ["season"]})
        seasons = seasons["result"]["seasons"]
    except:
        seasons = []

    return render_template('tv-show.html', **locals())


@app.route("/tv-shows/<int:show_id>/<int:season_id>")
def tv_show_seasons_episodes(show_id, season_id):
    """Compile all of the items necessary to show episodes for a selected TV show season, including:
    - List of episodes matching the season
    - Dictionary of TV show details

    Return a rendered template.
    """
    try:
        show = xbmc.VideoLibrary.GetTVShowDetails(
            {"tvshowid": show_id})["result"]["tvshowdetails"]
    except:
        show = {}
    try:
        seasons = xbmc.VideoLibrary.GetSeasons(
            {"tvshowid": show_id, "properties": ["season"]})
        seasons = seasons["result"]["seasons"]
    except:
        seasons = []

    try:
        episodes_list = xbmc.VideoLibrary.GetEpisodes({"tvshowid": show_id, "season": season_id, "sort": {
                                                      "order": "ascending", "method": "episode"}, "properties": ["thumbnail", "title", "showtitle", "season", "episode", "firstaired","playcount"]})
        episodes_result = episodes_list["result"]["episodes"]
        episodes = [episodes_result[i:i + 3]
                    for i in range(0, len(episodes_result), 3)]
    except:
        episodes = []

    return render_template('tv-show-episodes.html', **locals())


@app.route('/remote')
def remote():
    """Return the remote template"""
    return render_template('remote.html')


@app.route('/remote/playpause')
def remote_playpause():
    """Press the play/pause button"""
    xbmc.Player.PlayPause({"playerid": 0})
    xbmc.Player.PlayPause({"playerid": 1})
    return ''


@app.route('/remote/left')
def remote_left():
    """Press the left button."""
    xbmc.Input.Left()
    return ''


@app.route('/remote/right')
def remote_right():
    """Press the right button."""
    xbmc.Input.Right()
    return ''


@app.route('/remote/up')
def remote_up():
    """Press the up button."""
    xbmc.Input.Up()
    return ''


@app.route('/remote/down')
def remote_down():
    """Press the down button."""
    xbmc.Input.Down()
    return ''


@app.route('/remote/select')
def remote_select():
    """Press the select button."""
    xbmc.Input.Select()
    return


@app.route('/remote/rewind')
def remote_rewind():
    """Press the rewind button."""
    xbmc.Input.ExecuteAction({"action": "analogrewind"})
    return ''


@app.route('/remote/fastforward')
def remote_fastforward():
    """Press the fast forward button."""
    xbmc.Input.ExecuteAction({"action": "analogfastforward"})
    return ''


@app.route('/remote/previous')
def remote_previous():
    """Press the previous button."""
    xbmc.Player.GoTo({"to": "previous", "playerid": 1})
    return ''


@app.route('/remote/next')
def remote_next():
    """Press the next button."""
    xbmc.Player.GoTo({"to": "next", "playerid": 1})
    return ''


@app.route('/remote/stop')
def remote_stop():
    """Press the stop button."""
    xbmc.Player.Stop({"playerid": 1})
    return ''


@app.route('/remote/title')
def remote_title():
    """Press the context info button."""
    xbmc.Input.ContextMenu()
    return ''


@app.route('/remote/info')
def remote_info():
    """Press the info button."""
    xbmc.Input.Info()
    return ''


@app.route('/remote/menu')
def remote_menu():
    """Press the menu button."""
    xbmc.Input.ShowOSD()
    return ''


@app.route('/remote/back')
def remote_back():
    """Press the back button."""
    xbmc.Input.Back()
    return ''


@app.route('/seek/<int:seek_value>')
def seek_player(seek_value):
    """Seek the player to a specific point in the video."""

    # Multiply by the reducing factor of 5 to deal with actual seconds.
    seek_value = seek_value * 5

    # Turn seconds value into a value represented in hours, minutes, and
    # seconds.
    hours = seek_value / 3600
    minutes = (seek_value - (hours * 3600)) / 60
    seconds = seek_value - hours * 3600 - minutes * 60
    position = {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    # Send a seek request to the player.
    xbmc.Player.Seek({'playerid': 1, 'value': position})
    return ''


@app.route('/set/volume/<int:volume_value>')
def set_volume(volume_value):
    """Set the player volume to volume_value."""
    xbmc.Application.SetVolume({"volume": volume_value})
    return ''


def are_players_active():
    """Return true if players are active."""
    if xbmc.Player.GetActivePlayers()["result"]:
        return True


@app.route('/play/movie/<int:movie_id>')
def play_movie(movie_id):
    """Play a movie corresponding to movie_id."""
    xbmc.Playlist.Add({'item': {'movieid': movie_id}, 'playlistid': 1})
    xbmc.Player.Open({'item': {'movieid': movie_id}})
    return ''


@app.route('/enqueue/movie/<int:movie_id>')
def enqueue_movie(episode_id):
    """Add a movie to the playlist corresponding to movie_id."""
    xbmc.Playlist.Add({'item': {'movieid': movie_id}, 'playlistid': 1})
    return ''


@app.route('/play/episode/<int:episode_id>')
def play_episode(episode_id):
    """Play a TV show episode corresponding to episode_id."""
    xbmc.Playlist.Add({'item': {'episodeid': episode_id}, 'playlistid': 1})
    xbmc.Player.Open({'item': {'episodeid': episode_id}})
    return ''


@app.route('/enqueue/episode/<int:episode_id>')
def enqueue_episode(episode_id):
    """Add a TV show episode to the playlist corresponding to episode_id."""
    xbmc.Playlist.Add({'item': {'episodeid': episode_id}, 'playlistid': 1})
    return ''


@app.route('/play/trailer/<int:movie_id>')
def play_trailer(movie_id):
    """Retrieve the trailer URL for the movie from the database and open it in the player."""
    details = xbmc.VideoLibrary.GetMovieDetails(
        {"movieid": movie_id, "properties": ["trailer"]})
    trailer = details["result"]["moviedetails"]["trailer"]

    # Send opening request for trailer
    xbmc.Player.Open({'item': {'file': trailer}})
    return ''


def format_runtime(item_runtime, format="text"):
    """Format a runtime in seconds to a human readable format in hours and minutes.

    Takes a "format" argument that specifies whether the function should return:
    "text" -- "2 hr 7 min"
    "colon" -- "2:07:00"

    """
    if format == "text":
        if item_runtime > 3600:
            hours = item_runtime / 3600
            minutes = item_runtime / 60 - (hours * 60)
            if minutes == 0:
                newruntime = str(hours) + " hr "
            else:
                newruntime = str(hours) + " hr " + str(minutes) + " min"
        else:
            minutes = item_runtime / 60
            seconds = item_runtime - minutes * 60
            newruntime = str(minutes) + " min " + str(seconds) + " sec"
    if format == "colon":
        if item_runtime > 3600:
            hours = item_runtime / 3600
            minutes = item_runtime / 60 - (hours * 60)
            seconds = item_runtime - minutes * 60 - hours * 3600
            newruntime = str(
                hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        else:
            minutes = item_runtime / 60
            seconds = item_runtime - minutes * 60
            newruntime = str(minutes) + ":" + str(seconds).zfill(2)

    return newruntime


@app.route('/info/movie/<int:movie_id>')
def info_movie(movie_id):
    """Compile all of the items necessary to show information for a movie:
    - Dictionary of movie details

    Return a rendered template.
    """
    props = ["thumbnail", "originaltitle", "year", "runtime", "genre",
             "director", "cast", "plot", "trailer", "imdbnumber", "mpaa"]
    details = xbmc.VideoLibrary.GetMovieDetails(
        {"movieid": movie_id, "properties": props})
    movie = details["result"]["moviedetails"]

    # Format MPAA Rating to remove "Rating"
    movie["mpaa"] = movie["mpaa"].replace("Rated", "", 1)

    # Format the movie runtime into a human readable format
    movie["runtime"] = format_runtime(movie["runtime"])

    return render_template('info-movie.html', **locals())

@app.route('/movie/ask-resume/<int:movie_id>')
def ask_resume_movie(movie_id):
    """Get the resume point saved in the Kodi database for display to the user

    Return a rendered template.
    """
    props = ["thumbnail", "originaltitle", "year", "runtime", "genre",
             "resume"]
    details = xbmc.VideoLibrary.GetMovieDetails(
        {"movieid": movie_id, "properties": props})
    movie = details["result"]["moviedetails"]
    movie["runtime"] = format_runtime(movie["runtime"])
    resume_time = format_runtime(movie["resume"]["position"])

    return render_template('resume-movie.html', **locals())

@app.route('/episode/ask-resume/<int:episode_id>')
def ask_resume_episode(episode_id):
    """Get the resume point saved in the Kodi database for display to the user

    Return a rendered template.
    """
    props = ["thumbnail", "showtitle", "title", "season", "episode",
             "firstaired", "resume", "runtime"]
    details = xbmc.VideoLibrary.GetEpisodeDetails(
        {"episodeid": episode_id, "properties": props})
    episode = details["result"]["episodedetails"]
    episode["runtime"] = format_runtime(episode["runtime"])
    resume_time = format_runtime(int(episode["resume"]["position"]))

    return render_template('resume-episode.html', **locals())

@app.route('/resume/movie/<int:movie_id>')
def resume_movie(movie_id):
    """Start playing a movie at the resume point stored in the Kodi database"""
    xbmc.Playlist.Add({'item': {'movieid': movie_id}, 'playlistid': 1})
    xbmc.Player.Open({'item': {'movieid': movie_id}, "options":{'resume': True}})
    return ''

@app.route('/resume/episode/<int:episode_id>')
def resume_episode(episode_id):
    """Start playing an episode at the resume point stored in the Kodi database"""
    xbmc.Playlist.Add({'item': {'episodeid': episode_id}, 'playlistid': 1})
    xbmc.Player.Open({'item': {'episodeid': episode_id}, "options":{'resume': True}})
    return ''

@app.route('/info/episode/<int:episode_id>')
def info_episode(episode_id):
    """Compile all of the items necessary to show information for a TV episode:
    - Dictionary of episode details

    Return a rendered template.
    """
    props = ["thumbnail", "showtitle", "title", "plot",
             "cast", "runtime", "season", "episode", "firstaired"]
    details = xbmc.VideoLibrary.GetEpisodeDetails(
        {"episodeid": episode_id, "properties": props})
    episode = details["result"]["episodedetails"]

    # Format the movie runtime into a human readable format
    episode["runtime"] = format_runtime(episode["runtime"])

    return render_template('info-episode.html', **locals())

@app.route('/get_player_properties')
def get_player_properties():
    try:
        player_properties = xbmc.Player.GetProperties(
            {"playerid": 1, "properties": ["time", "percentage", "totaltime", "speed"]})["result"]
    except:
        player_properties = {"error": True}

    return jsonify(player_properties)

@app.route('/get_app_properties')
def get_app_properties():
    """Return a set of app properties to the client to convey current status of the Kodi application."""
    try:
        app_properties = xbmc.Application.GetProperties(
            {"properties": ["volume", "muted"]})["result"]
    except:
        app_properties = {"error": True}

    return jsonify(app_properties)


@app.route('/get_playing_properties')
def get_playing_properties():
    """Return a set of playing properties to the client to convey current status of the item which is playing."""
    try:
        playing_properties = xbmc.Player.GetItem({"playerid": 1, "properties": [
                                                 "title", "season", "episode", "showtitle", "thumbnail"]})["result"]
    except:
        playing_properties = {"error": True}

    return jsonify(playing_properties)

@app.route('/get_properties')
def get_properties():
    """Return a set of properties to the client to convey current status of the player.

    This includes three different types of properties:
    - Player properties indicating percentage complete, time elapsed, speed
    - App properties incidicating current volume and mute status
    - Playing properties giving the information of the currently playing item: season, episode, titles, etc.

    The properties are compiled into a single dictionary and returned in JSON format.
    """
    try:
        player_properties = xbmc.Player.GetProperties(
            {"playerid": 1, "properties": ["time", "percentage", "totaltime", "speed"]})["result"]
        app_properties = xbmc.Application.GetProperties(
            {"properties": ["volume", "muted"]})["result"]
        playing_properties = xbmc.Player.GetItem({"playerid": 1, "properties": [
                                                 "title", "season", "episode", "showtitle", "thumbnail"]})["result"]

        # Compile all of the properties into a single dictionary.
        properties = dict(
            player_properties.items() + app_properties.items() + playing_properties.items())

    except:
        properties = {"error": True}

    return jsonify(properties)


@app.route('/get_duration')
def get_duration():
    """Return the duration of the currently playing item in JSON format"""
    properties = xbmc.Player.GetProperties(
        {"playerid": 1, "properties": ["totaltime"]})
    return jsonify(properties)

@app.route('/movies/scan-library')
def scan_movie_library():
    """Send a request to Kodi to scan the movie library for updates.
    
    Return a redirect to the referrer. 
    """
    xbmc.VideoLibrary.Scan()
    return redirect(request.referrer)

@app.route('/movies/clean-library')
def clean_movie_library():
    """Send a request to Kodi to clean the movie library of non-existent items
    
    Return a redirect to the referrer. 
    """
    xbmc.VideoLibrary.Clean()
    return redirect(request.referrer)

@app.route('/movies/play-random')
def play_random_movie():
    """Select a random movie from the database and play it.

    Return a redirect to the referrer. 
    """
    movie_to_play = random.choice(get_all_movie_titles())
    play_movie(movie_to_play["movieid"])
    return redirect(request.referrer)

@app.route("/tv-shows/<int:show_id>/play-random/<int:season>")
def play_random_episode_from_season(show_id,season):
    """Select a random episode from the request season and playt it.

    Return a redirect to the referrer.
    """
    episode_to_play = random.choice(get_all_episodes_in_season(show_id, season))
    play_episode(episode_to_play["episodeid"])
    return redirect(request.referrer)

@app.route("/tv-shows/<int:show_id>/play-season/<int:season>")
def play_all_episodes_in_season(show_id, season):
    """Select a random episode from the request season and playt it.

    Return a redirect to the referrer.
    """
    episodes = get_all_episodes_in_season(show_id, season)
    play_episode(episodes[0]["episodeid"])
    for episode in episodes[1:]:
        enqueue_episode(episode["episodeid"])
    return redirect(request.referrer)

def get_all_episodes_in_season(show_id, season):
    """Return a list of all the episodes in season_id"""
    episodes_list = xbmc.VideoLibrary.GetEpisodes({"tvshowid": show_id, "season": season})
    episodes = episodes_list["result"]["episodes"]
    return episodes

def get_all_movie_titles():
    """Return a list of all the titles of the movies in the library."""
    movies = xbmc.VideoLibrary.GetMovies(
        {"properties": ["originaltitle"], "sort": {"order": "ascending", "method": "title"}})["result"]["movies"]
    return movies


def get_all_tv_show_titles():
    """Return a list of all the titles of the TV shows in the library."""
    tv_shows = xbmc.VideoLibrary.GetTVShows({"properties": ["title"], "sort": {
                                            "order": "ascending", "method": "title"}})["result"]["tvshows"]
    return tv_shows


@app.route('/debug/search_movies/<search_term>')
def debug_search_movies(search_term):
    """Return a list of movies matching the search term in JSON format."""
    return jsonify({'movies': search_movies(search_term)})


@app.route('/debug/search_tv/<search_term>')
def debug_search_tv(search_term):
    """Return a list of TV shows matching the search term in JSON format."""
    return jsonify({'tv_shows': search_tv_shows(search_term)})

@app.route('/get/resume_time/movie/<int:movie_id>')
def get_movie_resume_time_in_json(movie_id):
    """Return the resume time for the given Movie ID in JSON format."""
    return jsonify({'resume_time': get_movie_resume_time(movie_id)})

@app.route('/get/resume_time/episode/<int:episode_id>')
def get_episode_resume_time_in_json(episode_id):
    """Return the resume time for the given Episode ID in JSON format."""
    return jsonify({'resume_time': get_episode_resume_time(episode_id)})

def get_episode_resume_time(episode_id):
    """Return the resume time for the episode as given by the Kodi database"""
    resume_time = xbmc.VideoLibrary.GetEpisodeDetails({"episodeid": episode_id, "properties": ["resume"]})
    return resume_time["result"]["episodedetails"]["resume"]

def get_movie_resume_time(movie_id):
    """Return the resume time for the movie as given by the Kodi database"""
    resume_time = xbmc.VideoLibrary.GetMovieDetails({"movieid": movie_id, "properties": ["resume"]})
    return resume_time["result"]["moviedetails"]["resume"]


def search_movies(search_term):
    """Return a list of movies where 'search_term' is present within the title string."""

    # Get all of the movies from the database.
    movies = get_all_movie_titles()

    # Create a list of matching movies.
    matching_movies = []

    # Check each movie to see if its title matches the search term.
    for movie in movies:
        if search_term.lower() in movie["originaltitle"].lower():
            matching_movies.append(movie)
    return matching_movies


def search_tv_shows(search_term):
    """Return a list of TV shows where 'search_term' is present within the title string."""

    # Get all of the TV shows from the database.
    tv_shows = get_all_tv_show_titles()

    # Create a list of matching TV shows.
    matching_tv_shows = []

    # Check each show to see if its title matches the search term.
    for show in tv_shows:
        if search_term.lower() in show["title"].lower():
            matching_tv_shows.append(show)

    return matching_tv_shows


@app.route('/search')
def search_results():
    """Compile and return a list of media items matching the query as detailed in the GET request.

    Get the movies and TV shows in which the search term is seen inside the title and return
    a dictionary consisting of a list of TV shows and a list of movies and their details.

    Return a rendered template.
    """

    # Get the query as given as a GET parameter.
    search_term = request.args.get('query')

    # If the search term is empty or too short, compile empty lists and return
    # them.
    if search_term == '' or len(search_term) < 2:
        movies = []
        tv_shows = []
        size_error = True
        return render_template('search-results.html', **locals())

    # Search the database to get the IDs of the matching movies.
    movie_ids = search_movies(search_term)
    tv_show_ids = search_tv_shows(search_term)

    # Create empty lists to return.
    movies = []
    tv_shows = []

    # Query the database for each movie in the result and append the details
    # to the movie list.
    for movie in movie_ids:
        movie_details = xbmc.VideoLibrary.GetMovieDetails({"movieid": movie["movieid"], "properties": [
                                                          "originaltitle", "year", "plot", "thumbnail", "cast", "imdbnumber", "trailer"]})["result"]["moviedetails"]
        movies.append(movie_details)

    # Query the database for each TV show in the result and append the details
    # to the TV show list.
    for tv_show in tv_show_ids:
        seasons = xbmc.VideoLibrary.GetSeasons(
            {"tvshowid": tv_show["tvshowid"], "properties": ["season"]})["result"]
        tv_shows.append({"show": tv_show, "seasons": seasons})

    return render_template('search-results.html', **locals())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
