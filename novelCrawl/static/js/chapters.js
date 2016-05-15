$(document).ready(function() {
	var url = $("#url").val();
	$.get("/wonderland/book/getChapters", {url : url}).done(function(data){ 
		$("#title").text(data["title"]);
		$("#author").text(data["author"]);
		$("#title-container").css("visibility", "visible");
		$("#chapter-container").css("visibility", "visible");
		showChapters(data["chapters"]);
	})
	
	$("li").hover(function() {
        $(this).css('background-color', '#e6e6e6')
    }, function() {
        $(this).css('background-color', '')
    });
});


function showChapters(list) {
	var div = $("#chapter-container"); 
	for (var i = 0; i < list.length; i++) {
		var box = list[i];
		
		// add subtitle
		var subtitle = "<div class=\"box_title\">" +
					 		"<b>" + box["subtitle"] + "</b>" +
					   "</div>";
		$(div).append($(subtitle));
		
		// add title
		var chapter_list = $("<ul id=\"chapter-list\"></ul>");
		var chapters = box["chapters"];
		for (var j = 0; j < chapters.length; j++) {
			var chapter = chapters[j];
			var content = "<li class=\"chapter\">" + 
							"<b><a href=\"" + chapter["url"] + "\">" + chapter["chapter"] + "</a></b>" +
						  "</li>";
			$(chapter_list).append($(content));
		}
		$(div).append($("<div class=\"box_chapter\"><ul id=\"chapter-list\">" + $(chapter_list).html() + "</ul></div>"));
	}
}