
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var messages = [];
    sockets = [];


app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.broadcast.emit('chat display', 'a user connected');
  socket.emit('chat all', messages);

  socket.on('disconnect', function(){
    console.log('user disconnected');
    socket.broadcast.emit('chat display', 'a user disconnected');
  });

  socket.on('chat message', function(msg){
    console.log('message: ' + msg.msg);
    messages.push(msg);
    io.emit('chat message', msg);
  });

  socket.on('chat typer', function(msg){
    console.log('Typer: ' + JSON.stringify(msg));
    socket.broadcast.emit('chat typer', msg);
  });

});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
