$("#play").click(function() {
	$.get("/remote/playpause");
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
