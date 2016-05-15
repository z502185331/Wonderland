$(document).ready(function() {
	var url = $("#url").val();
	$.get("/wonderland/book/getChapters", {url : url}).done(function(data){ 
		$("#title").text(data["title"]);
		$("#author").text(data["author"]);
	})
});