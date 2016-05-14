$(document).ready(function(e) {
	$('.search-panel .dropdown-menu').find('a').click(function(e) {
		e.preventDefault();
		var param = $(this).attr("href").replace("#", "");
		var concept = $(this).text();
		$('.search-panel span#search_concept').text(concept);
		$('.input-group #search_param').val(param);
	});

	$("#search-btm").click(function(data) { // Search when clicking the button
		startSearch();
	})

	$("#kw-input").keypress(function(e) { // Search when clicking the enter on
		// keyboard
		if (e.which == 13) {
			startSearch();
		}
	});

	$(window).scroll(function() {  // Scroll down to the bottom and fresh more books
		if ($(window).scrollTop() + $(window).height() == getDocHeight() + 20) {
			furtherSearch();
		}
	});
});



/**
 * A function to get the height of documents. It fits all the web browsers
 * @returns the height of documents
 */
function getDocHeight() {
	var D = document;
	return Math.max(D.body.scrollHeight, D.documentElement.scrollHeight,
			D.body.offsetHeight, D.documentElement.offsetHeight,
			D.body.clientHeight, D.documentElement.clientHeight);
}

/**
 * Start searching
 */
function startSearch() {
	$("#booklist").empty();
	var type = $("#search_concept").text();
	var keyword = $("#kw-input").val();
	var startid = 0;
	
	// Save data to list
	var list = $("#booklist");
	list.data("keyword", keyword);
	list.data("type", type);	
	fetchBooks(keyword, type, startid);
	$("#kw-input").val('');
	$("#seperator").css("visibility", "visible");
	$("#keyword").text(keyword);
}

/**
 * Get more related books
 */
function furtherSearch() {
	var list = $("#booklist");
	var type = list.data("type");
	var keyword = list.data("keyword")
	var startid = list.data("startid") + 1;
	fetchBooks(keyword, type, startid);
}

/**
 * A function to search books, when clicking the button or 'enter' key
 */
function fetchBooks(keyword, type, startid) {
	$.get('search', {
		keyword : keyword,
		type : type,
		startid : startid
	}).done(function(data) {
		var books = data["books"];
		if ($("#booklist").data("startid") == undefined || 
				parseInt(data["startid"]) > $("#booklist").data("startid")) {
			$("#booklist").data("startid", parseInt(data["startid"]));
			appendBooks(books);
		}
	});
}

/**
 * A function to append the books into the book list
 * 
 * @param books
 *            the books
 */
function appendBooks(books) {
	var booklist = $("#booklist");
	for (var i = 0; i < books.length; i++) {
		var book = books[i];
		var content = "<li>" + "<div class=\"well\">" + "<div class=\"media\">"
				+ "<a class=\"pull-left\" href=\"#\">"
				+ "<img class=\"media-object\" src=\"" + book["cover"] + "\">"
				+ "</a>" + "<div class=\"media-body\">"
				+ "<h4 class=\"media-heading\">" + book["title"] + "</h4>"
				+ "<p class=\"text-right\">By " + book["author"] + "</p>"
				+ "<p>" + book["description"] + "</p>" + "</div>" + "</div>"
				+ "</div>" + "</li>";
		$(booklist).append(content);
	}

}
