$(document).ready(function() {	
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
	updateSlider();

	pBar.on("slideStart", function(slideEvt) {
		sliderTimer.pause();
	});
	pBar.on("slideStop", function(slideEvt) {
		sliderTimer.play();
		$.get('/seek/'+slideEvt.value);
	});

	var sliderTimer = $.timer(function() {
		updateSlider();
	}, 2000, true);

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

