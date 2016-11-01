

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

function dispatchSms(msg) {
  var smsParts = msg.split('\t')
  // cLog(smsParts)

  if (smsParts[1] == 'TestNode.ping') {
    sendSms(smsParts[1], smsParts[0], 'ACK')
  }
}

var net = require('net');

var client = new net.Socket();
var sysName = 'NodeClient'
client.connect(9999, '192.168.1.99', function() {
// client.connect(9999, 'localhost', function() {  
	console.log('Connected');

  sendSms(sysName, 'Serv.RegName', sysName)

  sendSms(sysName, 'TestNode.ping', '.')

	sendSms(sysName, 'Serv.CpuTemp', '.')
  sendSms(sysName, 'Serv.ping', '.')
  //sendSms(sysName, 'TestNode.Quit', sysName)
  //sendSms(sysName, 'Serv.UnRegName', sysName)

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
    dispatchSms(sms)

    data = data.slice(cnt  + 3)
  }
});

client.on('close', function() {
	console.log('Connection closed');
});