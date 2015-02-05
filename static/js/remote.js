$("#play").click(function() {
	$.get("/remote/playpause");
	$("#play").children(".fa").toggleClass('fa-play fa-pause');
});
$("#left").click(function() {
	$.get("/remote/left");
});
$("#right").click(function() {
	$.get("/remote/right");
});
$("#up").click(function() {
	$.get("/remote/up");
});
$("#down").click(function() {
	$.get("/remote/down");
});
$("#select").click(function() {
	$.get("/remote/select");
});
$("#rewind").click(function() {
	$.get("/remote/rewind");
	$("#play").children(".fa").toggleClass('fa-play fa-pause');
});
$("#fastforward").click(function() {
	$.get("/remote/fastforward");
	$("#play").children(".fa").toggleClass('fa-play fa-pause');
});
$("#previous").click(function() {
	$.get("/remote/previous");
});
$("#next").click(function() {
	$.get("/remote/next");
});
$("#stop").click(function() {
	$.get("/remote/stop");
});
$("#title").click(function() {
	$.get("/remote/title");
});
$("#info").click(function() {
	$.get("/remote/info");
});
$("#menu").click(function() {
	$.get("/remote/menu");
});
$("#back").click(function() {
	$.get("/remote/back");
});
