var socket = io.connect('http://' + document.domain + ":" + location.port);

socket.on('connect', function() { //Executed upon opening the site
  console.log('Successfully Connected');
})
