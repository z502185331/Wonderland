// Get the id of the chatroom
var roomHash = $("#roomHash").val();
var roomOwner = $("#roomOwner").val();
var lastFreshTime = "lastFreshTime";
var userList = []

// Enter the room
window.onload = function() {
	sessionStorage.setItem(lastFreshTime, (new Date()).getTime());
	console.log(roomHash + ":" + roomOwner);
	$.post('enterRoom/', {roomHash : roomHash, roomOwner : roomOwner}).done(function(data) {
		
		// Refresh the page
		refreshPage();
	});
}

//Leave the room
window.onbeforeunload = function () {
    $.post('leaveRoom/', {roomId : roomId}).done(function(data) {
    	console.log("Leave room " + roomId);
    });
//    return "Do you want to leave the chatroom?";
};




// Send a chat
$("#sendMsg").click(function() {
	var msg = $("#btn-input").val();
	$("#btn-input").val("");    // Clear the input
	
	// Send data to server
	$.post('sendMsg/', {roomHash : roomHash, msg : msg, time : (new Date()).getTime()}).done(function(data) {
		refreshPage();
	});
	
});

// Regularly refresh the page
(function poll() {
	setInterval(function() {
	      refreshPage();
	   }, 1000);
})();





/**
 * A function to refresh the page including the msg and current users in the chatroom
 */
function refreshPage() {
	
	// get last refresh time and store the current time
	var lastTime = sessionStorage.getItem(lastFreshTime);
	var currentTime = new Date();
	sessionStorage.setItem(lastFreshTime, currentTime.getTime());
	
	// Refresh msg
	$.get("getMsg/" + roomHash + "/" + lastTime).done(function(data) {
		var msgs = data["msgs"];
		appendMsg(msgs);
	});
	
	// Refresh user
	$.get("getUsers/" + roomHash).done(function(data){
		var users = data["users"];
		
		/* Add users who enter the room
		 * If username is in the userList, add to a temp list for later comparison */
		var temp = [];
		for (var i = 0; i < users.length; i++) {
			var user = users[i];
			var username = user["username"];
			if (userList.indexOf(username) < 0) {
				appendUsers(user)
			}
			temp.push(username);
		}
		
		/* Remove users who leave the room */
		for (var i = 0; i < userList.length; i++) {
			var username = userList[i];
			if (temp.indexOf(username) < 0) { // Leave the room
				removeUser(username);
			}
		}
	});
}

/**
 * A function to append the users on the page who enters the room
 * @param items a list of users
 */
function appendUsers(user) {
	var list = $(".userlist");
	var content = "<li id=\"user_" + user["username"] + "\" class=\"left clearfix\">" +
						"<span class=\"chat-img pull-left\">" +
							"<img src=\""+ user["icon"] +"\" alt=\"User Avatar\" class=\"img-circle\" />" +
						"</span>" +
						"<div class=\"name\">" +
							"<div class=\"header\">" +
								"<strong class=\"primary-font\">" + user["username"] + "</strong>" +
							"</div>" +
						"</div>" +
					"</li>";
    $(list).append($(content));	
    
    // Push the user into the userList
    userList.push(user["username"]);
}

/**
 * A function to remove a user who leaves from the room
 * @param username the name of user
 */
function removeUser(username) {
	$("#user_" + username).remove();
	
	// Remove a user from userList
	var index = userList.indexOf(username);
	userList.splice(index, 1);
}

/**
 * A function to append the new msgs to the list
 * @param msgs the new msgs
 */
function appendMsg(msgs) {
	var list = $("#msgList");
	for (var i = 0; i < msgs.length; i++) {
		var msg = msgs[i];
		var content = "<li class=\"left clearfix\">" +
							"<span class=\"chat-img pull-left\">" +
								"<img src=\"" + msg["icon"] + "\" alt=\"User Avatar\" class=\"img-circle\" />" +
							"</span>" +
							"<div class=\"chat-body clearfix\">" +
								"<div class=\"header\">" +
									"<strong class=\"primary-font\">" + msg["username"] + "</strong> <small class=\"pull-right text-muted\">" +
									"<span class=\"glyphicon glyphicon-time\"></span>" + formatTime(msg["time"]) + "</small>" +
								"</div>" +
								"<p>" + msg["content"] + "</p>" +
							"</div>" +
						"</li>";
		$(list).append($(content));
	}
}

/**
 * A method to format the millionseconds to time (hh:mm:ss)
 * @param time the millionseconds
 * @returns {String} a formatted string
 */
function formatTime(time) {
	var datetime = new Date(time);
	return datetime.getHours() + ":" + datetime.getMinutes() + ":" + datetime.getSeconds();
}



