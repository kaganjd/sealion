var url = 'http://127.0.0.1:5000/'

var socket = io.connect(url);
socket.on('connect', function() {
    socket.emit('connected', {data: 'Connected to p5'});
});

function setup() {
  createCanvas(400, 400);
  httpGet(url + 'payload', onData)
}

function onData(data) {
  console.log(data)
}
