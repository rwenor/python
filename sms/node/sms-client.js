

function cLog() {
  console.log(arguments)
}

cLog(1, "Hallo")

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function sendSms(fromMe, to, cmd) {
  s = fromMe +'\t'+ to +'\t'+ cmd
  s = pad(s.length,3) + s

  cLog(s, s.length)

  client.write(s)
}


var net = require('net');

var client = new net.Socket();
// client.connect(9999, '192.168.1.166', function() {
client.connect(9999, 'localhost', function() {  
	console.log('Connected');

  sendSms('TestNode', 'Serv.RegName', 'TestNode')
	sendSms('TestNode', 'Serv.CpuTemp', '.')
 
  sendSms('TestNode', 'TestNode.Quit', 'TestNode')
  sendSms('TestNode', 'Serv.UnRegName', 'TestNode')

});

client.on('data', function(data) {
	console.log('Received: ' + data);
	//client.destroy(); // kill client after server's response
});

client.on('close', function() {
	console.log('Connection closed');
});