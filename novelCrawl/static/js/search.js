$(document).ready(function(e){
    $('.search-panel .dropdown-menu').find('a').click(function(e) {
		e.preventDefault();
		var param = $(this).attr("href").replace("#","");
		var concept = $(this).text();
		$('.search-panel span#search_concept').text(concept);
		$('.input-group #search_param').val(param);
	});
    
    $("#search-btm").click(function(data) { // Search when clicking the button
    	onSearch();
    })
    
    $("#kw-input").keypress(function(e) { // Search when clicking the enter on keyboard
    	if (e.which == 13) {
    		onSearch();
    	}
    });
});

/**
 * A function to search books, when clicking the button or 'enter' key
 */
function onSearch() {
	var type = $("#search_concept").text();
	var keyword = $("#kw-input").val();
	$.get('search', {keyword : keyword, type : type}).done(function(data) {
		var books = data["books"];
		$("#seperator").css("visibility", "visible");
		$("#keyword").text(keyword);
		appendBooks(books);
	});
	$("#kw-input").val('');
	$("#booklist").empty();
}

/**
 * A function to append the books into the book list
 * @param books the books
 */
function appendBooks(books) {
	var booklist = $("#booklist");
	for (var i = 0; i < books.length; i++) {
		var book = books[i];
		var content = "<li>" +
						"<div class=\"well\">" +
							"<div class=\"media\">" +
								"<a class=\"pull-left\" href=\"#\">" +
									"<img class=\"media-object\" src=\"" + book["cover"] + "\">" +
								"</a>" +
								"<div class=\"media-body\">" +
									"<h4 class=\"media-heading\">" + book["title"] + "</h4>" +
									"<p class=\"text-right\">By " + book["author"] + "</p>" +
									"<p>" + book["description"] + "</p>" +
								"</div>" +
							"</div>" +
						 "</div>" +
					   "</li>";
		$(booklist).append(content);
	}
	
}

