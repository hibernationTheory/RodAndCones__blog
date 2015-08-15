var id = "post-header";
var el = document.getElementById(id);
if (el) {
	var path = '/static/blog/assets/particles.json'
	particlesJS.load(id, path);
}

$(function() {
	$(".post-bottom").each(function() {
		var that = this;
		$(this).siblings(".post-content").find("h1").after(function() {
			return new_el = $("<p class='post-date'>" + $(that).text() +"</p>");
		})
	});
});

