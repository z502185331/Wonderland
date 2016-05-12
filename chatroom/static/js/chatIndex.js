var currentUser = $("#currentUser").text()

loadAll();  // Init the page by loading all list


$("#toggleChoice").change(function(){
	if($(this).prop('checked')) {
		loadAll();
	} else {
		loadMine();
	}
});

// A function to load all chatrooms 
function loadAll() {
	$.get('allChatList/').done(function(data){
		var items = data["items"]
		refreshList(items)
		console.log("get data");
	});
}

// A function to load my chatrooms
function loadMine() {
	$.get('myChatList/').done(function(data){
		var items = data["items"]
		refreshList(items)
	});
}

//A function to clear and add all the chatrooms in items
function refreshList(items) {
	roomList = $("#roomList");
	$(roomList).empty(); // Clear the old rooms
	
	// replaced with new rooms
	for (var i = 0; i < items.length; i++) {
		var item = items[i];
		var content = "<li class=\"list-group-item\">" +
							"<span class=\"label label-default label-pill pull-right\">" + item["count"] + "</span>" +
							"<a href=\"chatroom/" + item["id"] + "\">" + item["title"] + "</a>" +
					  "</li> ";
		$(roomList).append($(content));
	}
}



//Open a new thread for chatroom
$("#createRoom").click(function(){
	var title = prompt("Please enter the title of your chatroom:", "");
	if (title.length != 0) {
		newThread(title);
	}
});

// A function to create a new chatroom
function newThread(title) {
	$.post('newRoom/', {title: title}).done(function(data){
		location.reload();
	});
}




