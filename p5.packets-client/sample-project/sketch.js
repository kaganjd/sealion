const hostname = "localhost";
const port = 8080;
const packet = new Sniffer(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(100, 255, 255);
  // 'Sniffer' name comes from Webpack output.library
  packet.getInterface();
  packet.runSniffer(5, "", "en0");
}

function draw() {
  packet.stopSniffer();
}
