let packet;
const hostname = "localhost";
const port = 8080;

function setup() {
  createCanvas(400, 400);
  background(100, 255, 255);
  // 'Sniffer' name comes from Webpack output.library
  packet = new Sniffer(hostname, port);
  packet.getInterface();
  packet.runSniffer();
  packet.configSniffer(2, "", "en0");
}

function draw() {}
