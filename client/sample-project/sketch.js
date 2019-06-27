// Instantiate a SeaLion instance with hostname and port
const hostname = "localhost";
const port = 8080;
const sl = new SeaLion(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(0);

  sl.mainSocket
    .open()
    .then(() => sl.getNetworkInfo())
    .then(() => sl.arpScan(sl.networkInfo.gw))
    .then(() => console.log(sl.arpTable));

  sl.sniffSocket.open().then(() => sl.sniffSelf(10));
}

function draw() {
  const lineHeight = 40;
  textSize(lineHeight);
  textAlign(LEFT, CENTER);

  if (sl.packetList) {
    for (i = 0; i < sl.packetList.length; i++) {
      fill(0, 255, 255);
      text(sl.packetList[i], 0, i * 40);
    }
  }
}
