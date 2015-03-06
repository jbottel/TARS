$(".imdbOpen").click(function() {
								window.open("//imdb.com/title/" + $(this).attr("data-imdb-number"));
});
$(".playMovie").click(function() {
								$.get("/play/movie/" + $(this).attr("data-movie-id"));
});
$(".enqueueMovie").click(function() {
								$.get("/enqueue/movie/" + $(this).attr("data-movie-id"));
});
$(".playEpisode").click(function() {
								$.get("/play/episode/" + $(this).attr("data-episode-id"));
});
$(".enqueueEpisode").click(function() {
								$.get("/enqueue/episode/" + $(this).attr("data-episode-id"));
});
$(".trailerMovie").click(function() {
								$.get("/play/trailer/" + $(this).attr("data-movie-id"));
});


