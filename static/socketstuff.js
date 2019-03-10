var socket = io.connect('http://' + document.domain + ":" + location.port);

socket.on('connect', function() {
  console.log('Successfully Connected');
})

socket.on('joinRoom', function(msg) {
  console.log(msg);
})

socket.on('message', function(msg) {
  console.log(msg);
})

var sendMessage = function() {
  console.log('Sending message');
  socket.send('hi im here');
}

var createRoom = function() {
  console.log('Creating room');
  socket.emit('createRoom',{ type:'chat', members:[] });
}
