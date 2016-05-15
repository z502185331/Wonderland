$(document).ready(function(e) {
	
	// Click the chapter button and show the chapter info
	$(".chapter-btn").click(function() {
		var chapter_id = $("#chapter_id").text();
		window.location.href = "/wonderland/book/chapters/" + chapter_id;
	})
});