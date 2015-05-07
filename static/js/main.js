$(document).ready(function() {	
	// Give focus to search bar
	$('#search-input').focus();

	// Run jquery.more on default shorten.
	$('.shorten').more({length: 125, moreText: "»", lessText: "«"});

	// Movie descriptions shorten
	$('.movie-desc').more({length: 105, moreText: "»", lessText: "«"});

	// Movie descriptions shorten
	$('.front-movie-desc, .episode-desc').more({length: 215, moreText: "»", lessText: "«"});

	$('.infoMovie').on('click', function(e) {
		var src = "/info/movie/" + $(this).attr('data-movie-id');
		$("#infoModal iframe").attr({'src':src});
	});
	$('.infoEpisode').on('click', function(e) {
		var src = "/info/episode/" + $(this).attr('data-episode-id');
		$("#infoModal iframe").attr({'src':src});
	});
	$(".info-iframe").load(function() {
		$(this).css("height", $(this).contents().height() + "px");
	});
	$("#remote-button").click(function() {
		$("#remoteDiv").toggle();
	});
	$("#play-pause-button").click(function() {
		$.get("/remote/playpause");

		if ($("#play-pause-button").hasClass("glyphicon-pause")) {
			$("#play-pause-button").removeClass("glyphicon-pause");
			$("#play-pause-button").addClass("glyphicon-play");
		}
		else {
			$("#play-pause-button").removeClass("glyphicon-play");
			$("#play-pause-button").addClass("glyphicon-pause");
		}
	});
	$("#stop-button").click(function() {
		$.get("/remote/stop");
	});

	var pBar = $("#progressbar").slider({
			formatter: function(value) {
				var secs = value*5;
				var hours = Math.floor(secs / 3600);
				var minutes = Math.floor((secs - hours*3600)/60);
				var secs = secs - (hours*3600) - (minutes*60);
				if (hours == 0) {
					return pad(minutes) + ":" + pad(secs);
				}
				else return hours + ":" + pad(minutes) + ":" + pad(secs);
			}
	});
	var vBar = $("#volumebar").slider();
	updateSlider();

	pBar.on("slideStart", function(slideEvt) {
		sliderTimer.pause();
	});
	pBar.on("slideStop", function(slideEvt) {
		sliderTimer.play();
		$.get('/seek/'+slideEvt.value);
	});

	vBar.on("slideStart", function(slideEvt) {
		sliderTimer.pause();
	});

	vBar.on("slideStop", function(slideEvt) {
		sliderTimer.play();
		$.get('/set/volume/'+slideEvt.value);
	});

	var sliderTimer = $.timer(function() {
		updateSlider();
	}, 2000, true);

	function pad(a){return(1e2+a+"").slice(-2)}

	function updateSlider() {
		$.getJSON('/get_properties','',function(data) {
			
			if (data.speed == 0) {
			$("#play-pause-button").removeClass("glyphicon-pause");
			$("#play-pause-button").addClass("glyphicon-play");
			}
			else {
			$("#play-pause-button").removeClass("glyphicon-play");
			$("#play-pause-button").addClass("glyphicon-pause");
			}
			if (data.volume) {
			vBar.slider('setValue',data.volume);
			}
			if (data.error) {
				pBar.slider('setAttribute','max',100);
				pBar.slider('setValue',0);
				$("#secdisp").html("0:00 / 0:00");
				$("#tv-show-title").html("<span style='padding-right: 11em;'></span>");
				$("#episode-title").html("&nbsp;");
				return;
			}
			if (data.item.type == "episode") {
				var tvShowTitle = data.item.showtitle;
				var displayTVShowTitle = tvShowTitle;
				if (tvShowTitle.length > 18) displayTVShowTitle = tvShowTitle.substring(0,18) + "...";
				var showTitleHTML = "<span title='" + tvShowTitle + "'>" + displayTVShowTitle + "</span>";
				$("#tv-show-title").html(showTitleHTML);
				var episodeTitle = "S" + data.item.season + "E" + data.item.episode + " - " + data.item.title;
				var displayTitle = episodeTitle;
				if (episodeTitle.length > 18) displayTitle = episodeTitle.substring(0,18) + "...";
				var titleHTML = "<span title='" + episodeTitle + "'>" + displayTitle + "</span>";
				$("#episode-title").html(titleHTML);
			}
			else if (data.item.type == "movie") {
				var movieTitle = data.item.title;
				var displayMovieTitle = movieTitle;
				if (movieTitle.length > 18) displayMovieTitle = movieTitle.substring(0,18) + "...";
				var movieTitleHTML = "<span title='" + movieTitle + "'>" + displayMovieTitle + "</span>";
				$("#tv-show-title").html(movieTitleHTML);
				$("#episode-title").html("");
			}
			else if (data.item.type == "unknown") {
				var itemTitle = data.item.title;
				var displayTitle = itemTitle;
				if (itemTitle.length > 17) displayTitle = itemTitle.substring(0,17) + "...";
				var titleHTML = "<span title='" + itemTitle + "'>" + displayTitle + "</span>";
				$("#tv-show-title").html(titleHTML);
				$("#episode-title").html("");
			}
			else {
				$("#tv-show-title").html("");
				$("#episode-title").html("");
			}


			var setMax = ((data.totaltime.hours *3600) + (data.totaltime.minutes * 60) + data.totaltime.seconds) / 5;
			console.log("setMax"+setMax);
			pBar.slider('setAttribute','max',setMax);
			var newVal = setMax * (data.percentage / 100);
			pBar.slider('setValue',newVal);
			if (data.totaltime.hours == 0) 
			{
				var curTime = ""+pad(data.time.minutes)+":"+pad(data.time.seconds);
				var fullTime  = ""+pad(data.totaltime.minutes)+":"+pad(data.totaltime.seconds);
			}
			else {
				var curTime = ""+data.time.hours+":"+pad(data.time.minutes)+":"+pad(data.time.seconds);
				var fullTime  = ""+data.totaltime.hours+":"+pad(data.totaltime.minutes)+":"+pad(data.totaltime.seconds);
			}
			$("#secdisp").html(curTime+" / "+fullTime);
		});
	}
});

