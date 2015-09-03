$(".imdbOpen").click(function() {
	window.open("//imdb.com/title/" + $(this).attr("data-imdb-number"));
});
$(".playMovie").click(function() {
	var movie_id = $(this).attr("data-movie-id");
	console.log(movie_id);
	$.getJSON("/get/resume_time/" + movie_id,'', function(data) {
		console.log(data);	
		if (data.resume_time.position == 0) {
			$.get("/play/movie/" + movie_id);
		}
		else {
			console.log("I should resume");
			var src = "/movie/ask-resume/" + movie_id;
			console.log(src);
			$("#infoModal iframe").attr({'src':src});
			$("#infoModal").modal('show');
		}
	}
	
	);
});

$(".forcePlayMovie").click(function() {
	var movie_id = $(this).attr("data-movie-id");
	$.get("/play/movie/" + movie_id);
	parent.$("#infoModal").modal('hide');
});

$(".resumeMovie").click(function() {
	var movie_id = $(this).attr("data-movie-id");
	$.get("/resume/movie/" + movie_id);
	parent.$("#infoModal").modal('hide');
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


