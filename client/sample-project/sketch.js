const hostname = "localhost";
const port = 8080;
// 'Sniffer' name comes from Webpack output.library
const packet = new Sniffer(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(0);

  packet.getNetworkInfo()
  
  // arp
  // packet.arpScan("192.168.0.50");

  // sniff
  // packet.sniffSelf(5);
  // packet.sniffNeighbor(25, "192.168.0.51");
}

function draw() {
  console.log(packet.networkInfo)
  textSize(20)
  for (i=0; i < 10; i++) {
    // console.log(packet.arpTable)
    fill(0, 255, 255);
    text(packet.arpTable[i].mac, (width/10) * i, (height/10) * i + 10)
    fill(255, 0, 255);
    text(packet.arpTable[i].mac, (width/10) * i + 2, (height/10) * i + 12)
  }
}


