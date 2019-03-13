var socket = io.connect('http://' + document.domain + ":" + location.port);
var submitNameBtn = document.getElementById('newNameBtn');
var nameinput = document.getElementById('newName');
var msgbox = document.getElementById('msgtosend');
var roombox = document.getElementById('roomtojoin');

socket.on('connect', function() { //Executed upon opening the site
  console.log('Successfully Connected');
  console.log('Joining General');
  socket.emit('setName', 'CoolBean'); //Default name
  $('#nameModal').modal() //Opens name prompt
})

socket.on('joinRoom', function(msg) { //Executed upon recieving a joinRoom event
  console.log("Successfully joined " + msg);
})

socket.on('message', function(msg) { //Executed upon recieving a message event
  var chatlog = document.getElementById('chatlog');
  var newMsg = document.createElement('li');
  var children = chatlog.children;
  if (children.length > 10) {
    chatlog.removeChild(children[0]);
  }
  newMsg.innerHTML = msg; //Sets new list item to reflect the message recieved
  chatlog.appendChild(newMsg) //Append the new element to the chat list
})

var sendMessage = function() { //Sends a message event to the server
  console.log('Sending message');
  var newMsg = msgbox.value;
  console.log(newMsg);
  socket.send(newMsg);
  msgbox.value = "";
}

var joinRoom = function() { //Sends an event to the server to join a room
  console.log('Joining room');
  inputbox = document.getElementById('roomtojoin');
  var roomName = inputbox.value;
  socket.emit('joinRoom',roomName);
  inputbox = "";
}

var submitName = function() {
  console.log('Setting name to ' + nameinput.value);
  socket.emit('setName', nameinput.value);
  var closebtn = document.getElementById('closemodal');
  socket.emit('joinRoom', 'General'); //Sends the joinRoom event to the server, with the data 'General'
  $('#nameModal').modal('hide')
}

nameinput.addEventListener("keydown", function(event) {
  if (event.keyCode == 13) {
    event.preventDefault();
    submitNameBtn.click();
  }
})

msgbox.addEventListener("keydown", function(event) {
  if (event.keyCode == 13) {
    event.preventDefault();
    sendMessage();
  }
})

roombox.addEventListener("keydown", function(event) {
  if (event.keyCode == 13) {
    event.preventDefault();
    joinRoom();
  }
})
