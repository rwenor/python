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

  if (cmd == 'DisCon') {
    cLog('Fake')
  }
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

  if (smsParts[1] == sysName) {
    cLog('SysMsg:', smsParts[2])
    //sendSms(smsParts[1], smsParts[0], 'ACK')
    if (smsParts[2] == 'BYE') {
      setTimeout( () => {
        process.exit(0)
      }, 500)
    }

    if (smsParts[2] == 'DisCon') {
      setTimeout( () => {
        client.destroy()
        //client = new net.Socket()
      }, 500)
    }

  }
}


// print process.argv
cLog('Args:')
process.argv.forEach(function (val, index, array) {
  console.log('  ', index + ': ' + val);
});


function sendConnect() {
  console.log('Connected')
  isConnected = 1
  sendSms(sysName, 'Serv.RegName', sysName)

  sendSms(sysName, 'TestNode.ping', '.')

	sendSms(sysName, 'Serv.CpuTemp', '.')
  sendSms(sysName, 'Serv.ping', '.')
  //sendSms(sysName, 'TestNode.Quit', sysName)
  //sendSms(sysName, 'Serv.UnRegName', sysName)
  setTimeout(() => {
    //sendSms(sysName, sysName, 'DisCon')
  }, 1000)
}

// ****** MAIN ******
var net = require('net');
var client = new net.Socket();

var myArgs = process.argv.slice(2)
var sysName = myArgs[1] || 'NodeClient'
var servIp = myArgs[0] || '192.168.1.166'
var isConnected = 0

cLog('Connecting: ', servIp)

client.connect(9999, servIp, function() {
// client.connect(9999, 'localhost', function() {  
  sendConnect()
});

client.on('error', function(e) {
    if(e.code == 'ECONNREFUSED') {
        console.log('Is the server running?');

        setTimeout(function() {
            client.connect(9999, servIp, function(){
                console.log('RECONNECTED TO: ' + servIp + ':' + 9999);
                sendConnect()
            });
        }, 4000);

        console.log('Timeout for 5 seconds before trying port:' + 9999 + ' again');
    }  
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
  if (isConnected) {
    console.log('Connection closed ??? Reconnect');

    setTimeout(function() {
            client.connect(9999, servIp, function(){
                console.log('RECONNECTED TO: ' + servIp + ':' + 9999);
                sendConnect()
            });
    }, 4000);

  } else {
    console.log('??? Reconnect');
  }
  
  isConnected = 0
});


process.addListener('SIGINT', function () {
  cLog('The end...')
  // sendSms(sysName, 'Serv.Quit', sysName)
  sendSms(sysName, 'Serv.UnRegName', sysName)
  
  // setTimeout( () => {
  //   process.exit(0)
  // }, 500)
  
})