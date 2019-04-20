---
id: examples-arp-table
title: Arp Table
sidebar_label: Arp Table
---
```js
// Instantiate a SeaLion instance with hostname and port
const hostname = "localhost";
const port = 8080;
const sl = new SeaLion(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(0);
  sl.socket.open()
    .then(() => sl.getNetworkInfo())
    .then(networkResults => sl.arpScan(networkResults.gw))
}

function draw() {
  // Create some text settings
  const lineHeight = 40
  textSize(lineHeight)
  textAlign(LEFT, CENTER)

  if (sl.arpTable) {
    for (i=0; i < 5; i++) {
      fill(0, 255, 255);
      text(sl.arpTable[i]['mac'], 0, 40*i)
      fill(255, 0, 255);
      text(sl.arpTable[i]['mac'], 2, 40*i + 2)
    }
  }
}
```
