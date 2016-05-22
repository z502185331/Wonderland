$(document).ready(function(e) {
	
	// Click the chapter button and show the chapter info
	$(".chapter-btn").click(function() {
		var bookid = $("#bookid").text();
		var source = $("#source").text();
		window.location.href = "/wonderland/book/chapters?url=" + bookid + "&source=" + source;
	})
});