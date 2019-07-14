// Instantiate a SeaLion instance with hostname and port
const hostname = "localhost";
const port = 8080;
const sl = new SeaLion(hostname, port);

packets = [];

function setup() {
  createCanvas(400, 400);
  background(0);
  sl.sniffer.start("192.168.7.189");
}

sl.sniffer.listener.on("packet", function(data) {
  packets.push(data);
});

function draw() {
  if (packets.length === 5) {
    drawPackets();
  }
}

function drawPackets() {
  textSize(40);
  textAlign(LEFT, CENTER);
  for (i = 0; i < 6; i++) {
    fill(0, 255, 255);
    text(packets[i], 0, i * 40);
  }
  sl.sniffer.close();
}
