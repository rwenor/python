

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
  sendSms('TestNode', 'Serv.ping', '.')
 
  sendSms('TestNode', 'TestNode.ping', '.')
  sendSms('TestNode', 'TestNode.Quit', 'TestNode')
  sendSms('TestNode', 'Serv.UnRegName', 'TestNode')

});

function myAssert(condition, message) {
    if (!condition) {
        message = message || "Assertion failed";
        if (typeof Error !== "undefined") {
            throw new Error(message);
        }
        throw message; // Fallback
    }
}

client.on('data', function(data) {
 
  // Split up messages 
  while (data.length > 0)  { 
    var cnt = +data.slice(0,3)
    myAssert(cnt <= data.length - 3)

    var sms = data.slice(3, cnt + 3).toString('utf8')

    console.log('Received msg: ' + sms);

    data = data.slice(cnt  + 3)
  }
});

client.on('close', function() {
	console.log('Connection closed');
});