
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendfile('index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.broadcast.emit('chat display', 'a user connected');

  socket.on('disconnect', function(){
    console.log('user disconnected');
    socket.broadcast.emit('chat display', 'a user disconnected');
  });

  socket.on('chat message', function(msg){
    console.log('message: ' + msg);
    socket.broadcast.emit('chat message', msg);
  });

  socket.on('chat typer', function(msg){
    console.log('message: ' + msg);
    socket.broadcast.emit('chat typer', msg);
  });

});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
