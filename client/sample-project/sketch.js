// Instantiate a SeaLion instance with hostname and port
const hostname = "localhost";
const port = 8080;
// const sl = new SeaLion(hostname, port);

packets = [];
// default IP address
var IP2Sniff;
var sl;
var sniffXPosition;

function setup() {
  createCanvas(400, 400);
  background(120);

  // sl.sniffer.start();

  // field for inputting IP address
  let IPField = createInput("type IP address to sniff");
  IPField.position(10, height - 12);
  IPField.input(writeIP);
  // button to initiate sniffing
  let sniffButton = createButton("Sniff");
  sniffButton.position(10 + IPField.size().width, height - 12);
  sniffButton.mousePressed(openSniff);
  sniffXPosition = sniffButton.size().width;
}

function openSniff() {
  sl = new SeaLion(hostname, port);
  sl.sniffer.listener.on("packet", function(data) {
    packets.push(data);
  });
  sl.sniffer.start(IP2Sniff);
  let closeButton = createButton("Stop");
  closeButton.position(sniffXPosition + 10, height - 12);
  closeButton.mousePressed(cleanUpSniffer);
}

function writeIP() {
  IP2Sniff = this.value();
}

function cleanUpSniffer() {
  sl.sniffer.stop();
  sl.mainSocket.close();
}

function draw() {
  if (packets.length === 5) {
    drawPackets();
  }
}

function drawPackets() {
  textSize(14);
  textAlign(LEFT, CENTER);
  for (i = 0; i < 20; i++) {
    fill(0, 255, 255);
    text(packets[i], 0, i * 40 + 30);
  }
}
