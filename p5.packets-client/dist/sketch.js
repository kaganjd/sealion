let packet;
const hostname = "localhost";
const port = 8080;

function setup() {
  createCanvas(400, 400);
  background(100, 255, 255);
  packet = new Sniffer(hostname, port);
  console.log(packet);
  packet.open();
  packet.monitor();
}

function draw() {}
