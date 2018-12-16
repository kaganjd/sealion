const hostname = "localhost";
const port = 8080;
const packet = new Sniffer(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(100, 255, 255);
  // 'Sniffer' name comes from Webpack output.library

  // get network info; goes with arpScan() alternative below
  // packet.getNetworkInfo()
  //             .then(data => networkInfo.push(data))
  packet.getNetworkInfo();
  // arp
  packet.arpScan("192.168.1.50");

  // sniff
  // packet.sniffSelf(5);
  // packet.sniffNeighbor(25, "192.168.0.51");
}

function draw() {}

console.log(packet.networkInfo);
