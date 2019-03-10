var socket = io.connect('http://' + document.domain + ":" + location.port);

socket.on('connect', function() {
  console.log('Successfully Connected');
  console.log('Joining General');
  socket.emit('joinRoom', 'General');
})

socket.on('joinRoom', function(msg) {
  console.log(msg);
})

socket.on('message', function(msg) {
  var chatlog = document.getElementById('chatlog');
  var newMsg = document.createElement('li');
  var children = chatlog.children;
  newMsg.innerHTML = msg;
  chatlog.appendChild(newMsg)
})

var sendMessage = function() {
  console.log('Sending message');
  inputbox = document.getElementById('msgtosend');
  var newMsg = inputbox.value;
  console.log(newMsg);
  socket.send(newMsg);
  inputbox.value = "";
}

var joinRoom = function() {
  console.log('Joining room');
  inputbox = document.getElementById('roomtojoin');
  var roomName = inputbox.value;
  socket.emit('joinRoom',roomName);
  inputbox = "";
}
