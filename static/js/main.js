$(document).ready(function() {	
								$("#remote-button").click(function() {
																$("#remoteDiv").toggle();
								});
								var pBar = $("#progressbar").slider();
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

								window.setInterval(function() {
																updateSlider();
								}, 2500);

								function pad(a){return(1e2+a+"").slice(-2)}

								function updateSlider() {
																$.getJSON('/get_properties','',function(data) {
																								if (data.error) {
																																pBar.slider('setAttribute','max',100);
																																pBar.slider('setValue',0);
																																$("#secdisp").html("0:00 / 0:00");
																																return;
																								}

																								var setMax = ((data.result.totaltime.hours *3600) + (data.result.totaltime.minutes * 60) + data.result.totaltime.seconds) / 5;
																								console.log("setMax"+setMax);
																								pBar.slider('setAttribute','max',setMax);
																								var newVal = setMax * (data.result.percentage / 100);
																								pBar.slider('setValue',newVal);
																								if (data.result.totaltime.hours == 0) 
																								{
																																var curTime = ""+pad(data.result.time.minutes)+":"+pad(data.result.time.seconds);
																																var fullTime  = ""+pad(data.result.totaltime.minutes)+":"+pad(data.result.totaltime.seconds);
																								}
																								else {
																																var curTime = ""+data.result.time.hours+":"+pad(data.result.time.minutes)+":"+pad(data.result.time.seconds);
																																var fullTime  = ""+data.result.totaltime.hours+":"+pad(data.result.totaltime.minutes)+":"+pad(data.result.totaltime.seconds);
																								}
																								$("#secdisp").html(curTime+" / "+fullTime);
																});
								}
});

