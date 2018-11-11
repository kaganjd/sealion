const hostname = "localhost";
const port = 8080;
const packet = new Sniffer(hostname, port);
let networkInfo = [];

function setup() {
  createCanvas(400, 400);
  background(100, 255, 255);
  // 'Sniffer' name comes from Webpack output.library

  // get network info; goes with arpScan() alternative below
  // packet.getInterface()
  //             .then(data => networkInfo.push(data))

  // arp
  packet
    .getInterface()
    .then(getInterfaceObj => packet.arpScan(getInterfaceObj.ifaddr))
    .then(arpResults => console.log(arpResults));

  // sniff
  packet.sniffSelf(5, "", "en0");
  packet.sniffNeighbor("192.168.1.1", 25);
}

function draw() {
  // arp()
}

// arpScan() alternative if you want to avoid promises
// function arp() {
//   if (networkInfo.length > 0) {
//     let myIp = networkInfo[0].ifaddr
//     packet.arpScan(myIp)
//   }
// }
