//require the express module
const express = require("express");
const app = express();
const dateTime = require("simple-datetime-formater");
const bodyParser = require("body-parser");
const chatRouter = require("./route/chatroute");
const loginRouter = require("./route/loginRoute");

const con = require("./dbconnect");
//require the http module
const http = require("http").Server(app);

// require the socket.io module
const io = require("socket.io");

const port = 8080;

//bodyparser middleware
app.use(bodyParser.json());

//routes
app.use("/chats", chatRouter);
app.use("/login", loginRouter);

//set the express.static middleware
app.use(express.static(__dirname + "/public"));

//integrating socketio
socket = io(http);

//database connection
const Chat = require("./models/Chat");

//setup event listener
socket.on("connection", socket => {
  console.log("user connected");

  socket.on("disconnect", function () {
    console.log("user disconnected");
  });

  //Someone is typing
  socket.on("typing", data => {
    socket.broadcast.emit("notifyTyping", {
      user: data.user,
      message: data.message
    });
  });

  //when soemone stops typing
  socket.on("stopTyping", () => {
    socket.broadcast.emit("notifyStopTyping");
  });

  socket.on("chat message", function (msg, from, to) {
    //broadcast message to everyone in port:5000 except yourself.
    socket.broadcast.emit("received", { message: msg, senderId: from, receiverId: to });
    var sql = "INSERT INTO chat_tbl (sender, receiver, message, send_time) VALUES ('"+from+"', '"+to+"', '"+msg+"', +'" + new Date().toISOString().slice(0, 19).replace('T', ' ') + "')";
    con.query(sql, function (err, result) {
      if (err) throw err;
      console.log("1 record inserted");
    });
  });
});

http.listen(port, () => {
  console.log("Running on Port: " + port);
});
