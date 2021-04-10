var socket = io();
var messages = document.getElementById("messages");

(function() {
  $("form").submit(function(e) {
    let li = document.createElement("li");
    e.preventDefault(); // prevents page reloading
    socket.emit("chat message", $("#message").val(), $("#from").val(), $("#to").val());

    messages.appendChild(li).append($("#message").val());
    let span = document.createElement("span");
    messages.appendChild(span).append("by " + $("#from").val() + ": " + "just now");

    $("#message").val("");

    return false;
  });

  socket.on("received", data => {
    if((data.senderId == $("#from").val() || data.senderId==$("#to").val()) && (data.receiverId == $("#from").val() || data.receiverId==$("#to").val())) {
      let li = document.createElement("li");
      let span = document.createElement("span");
      var messages = document.getElementById("messages");
      messages.appendChild(li).append(data.message);
      messages.appendChild(span).append("by " + data.senderId + ": " + "just now");
    }
  });
})();

// fetching initial chat messages from the database
(function() {
  fetch("/chats")
    .then(data => {
      return data.json();
    })
    .then(json => {
      console.log(json, "JSON")
      json.map(data => {
        let li = document.createElement("li");
        let span = document.createElement("span");
        if((data.senderId == $("#from").val() || data.senderId==$("#to").val()) && (data.receiverId == $("#from").val() || data.receiverId==$("#to").val())) {
          messages.appendChild(li).append(data.message);
          messages.appendChild(span).append("by " + data.senderId + ": " + formatTimeAgo(data.createdAt));
        } 
      });
    });
})();

//is typing...

let messageInput = document.getElementById("message");
let typing = document.getElementById("typing");

//isTyping event
messageInput.addEventListener("keypress", () => {
  socket.emit("typing", { user: "Someone", message: "is typing..." });
});

socket.on("notifyTyping", data => {
  typing.innerText = data.user + " " + data.message;
  console.log(data.user + data.message);
});

//stop typing
messageInput.addEventListener("keyup", () => {
  socket.emit("stopTyping", "");
});

socket.on("notifyStopTyping", () => {
  typing.innerText = "";
});
