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
  sl = new SeaLion(hostname, port);

  // field for inputting IP address
  let IPField = createInput("type IP address to sniff");
  IPField.position(10, height - 12);
  IPField.input(writeIP);
  // button to initiate sniffing
  let sniffButton = createButton("Sniff");
  sniffButton.position(10 + IPField.size().width, height - 12);
  sniffButton.mousePressed(openSniff);
  sniffXPosition = sniffButton.size().width + 10 + IPField.size().width;
  // button to get network info and draw the resulting ARP table
  let getNetInfoButton = createButton("Get Net Info");
  getNetInfoButton.position(
    10 + sniffButton.width + IPField.width,
    height - 12
  );
  getNetInfoButton.mousePressed(getInfo);
}

function openSniff() {
  sl.initSniffer(IP2Sniff);
  sl.sniffer.listener.on("packet", function(data) {
    packets.push(data);
  });

  let closeButton = createButton("Stop");
  closeButton.position(sniffXPosition + 10, height - 12);
  closeButton.mousePressed(cleanSniff);
}

function getInfo() {
  sl.getNetworkInfo().then(results => sl.arpScan(results.ifaddr));
}

function writeIP() {
  IP2Sniff = this.value();
}

function cleanSniff() {
  sl.clear();
}

function draw() {
  if (packets.length > 5) {
    drawPackets();
  }
  if (sl.arpTable) {
    drawArpTable();
  }
}

function drawArpTable() {
  textSize(20);
  textAlign(LEFT, TOP);
  for (i = 0; i < sl.arpTable.length; i++) {
    fill(0, 255, 255);
    text(sl.arpTable[i]["mac"], 0, 40 * i);
    fill(255, 0, 255);
    text(sl.arpTable[i]["mac"], 2, 40 * i + 1);
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
