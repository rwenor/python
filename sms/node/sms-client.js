//
// <cmd> <ip-server> <client-name>
//

function cLog(...arg) {
  // console.log(arguments)
  console.log(...arg)
}

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function myAssert(condition, message) {
    if (!condition) {
        message = message || "Assertion failed";
        if (typeof Error !== "undefined") {
            throw new Error(message);
        }
        throw message; // Fallback
    }
}

// **** Sms Func ****
function sendSms(fromMe, to, cmd) {
  s = fromMe +'\t'+ to +'\t'+ cmd
  s = pad(s.length,3) + s

  cLog('<sendSms', s, s.length, '</>')

  client.write(s)
}


// ***** DISPATCH *****
function dispatchSms(msg) {
  var smsParts = msg.split('\t')
  // cLog(smsParts)

  if (smsParts[1] == sysName +'.ping') {
    cLog('ping...')
    sendSms(smsParts[1], smsParts[0], 'ACK')
  }
}


// print process.argv
cLog('Args:')
process.argv.forEach(function (val, index, array) {
  console.log('  ', index + ': ' + val);
});

// ****** MAIN ******
var net = require('net');
var client = new net.Socket();

var myArgs = process.argv.slice(2)
var sysName = myArgs[1] || 'NodeClient'
var servIp = myArgs[0] || '192.168.1.166'

cLog('Connecting: ', servIp)

client.connect(9999, servIp, function() {
// client.connect(9999, 'localhost', function() {  
	console.log('Connected');

  sendSms(sysName, 'Serv.RegName', sysName)

  sendSms(sysName, 'TestNode.ping', '.')

	sendSms(sysName, 'Serv.CpuTemp', '.')
  sendSms(sysName, 'Serv.ping', '.')
  //sendSms(sysName, 'TestNode.Quit', sysName)
  //sendSms(sysName, 'Serv.UnRegName', sysName)

});

// Split and send to dispatcher
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

// Close
client.on('close', function() {
	console.log('Connection closed');
});
