// Instantiate a SeaLion instance with hostname and port

const hostname = "localhost";
const port = 8080;
const sl = new SeaLion(hostname, port)

function setup() {
  createCanvas(400, 400);
  background(0);
  sl.socket.open()
    .then(() => sl.getNetworkInfo())
    .then(result => console.log(result))
    .then(() => sl.socket.close())
}

// function draw() {
//   // Create some text settings
//   const lineHeight = 20
//   textSize(lineHeight)
//   textAlign(LEFT, CENTER)
//   // Check if networkInfo has been populated by getNetworkInfo() yet by seeing if the 'gw' key exists
//   if (sl.networkInfo) {
//     // Draw the gateway in one corner of the canvas
//     const gwString = `Router 👾 ${sl.networkInfo.gw}`
//     const gwStringWidth = textWidth(gwString)
//     fill(0, 255, 255);
//     text(gwString, 0, lineHeight)
//     // And your computer in the other corner
//     const ifaddrString = `My computer 💻 ${sl.networkInfo.ifaddr}`
//     const ifaddrStringWidth = textWidth(ifaddrString)
//     fill(255, 204, 0);
//     text(ifaddrString, width - ifaddrStringWidth, height - lineHeight)
//   }
// }
