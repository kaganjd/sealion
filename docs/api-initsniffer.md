---
id: api-initsniffer
title: initSniffer Method
sidebar_label: initSniffer
---

This method initializes a sniffer to start sniffing at the IP address passed in to the function. If no IP address is passed in, the sniffer defaults to sniffing traffic on your computer's current IP address.

Under the hood, this method establishes a websocket connection to the server, which the server uses to send packets to the client. It also sets up an event emitter, which the client can use to listen for incoming packets.

## Usage

```js
.initSniffer(ipAddress)
```

> Start sniffing traffic on the IP address passed in. If no IP address is passed in, the sniffer defaults to sniffing traffic on your computer's current IP address.

### Parameters

`ipAddress` _String_ (optional). A valid IP address on your subnet.

### Examples

```js
// Start sniffing traffic at 172.17.32.175
sl.initSniffer("172.17.32.175");
```

```js
// Start sniffing your own computer's traffic
sl.initSniffer();
```

### Complete example

```js
const hostname = "localhost";
const port = 8080;
let sl;
const packets = [];

function setup() {
  createCanvas(400, 400);
  background(120);

  // Create a Sea Lion instance at the given hostname and port
  sl = new SeaLion(hostname, port);

  // Create a button that calls startSniff
  let startButton = createButton("Start");
  startButton.position(10, 10);
  startButton.mousePressed(startSniff);
}

function startSniff() {
  // Initialize the sniffer with an IP address
  // Set up the packet event listener that adds each incoming packet to the packets array
  sl.initSniffer();
  sl.sniffer.listener.on("packet", function(data) {
    packets.push(data);
  });

  // Create a button that calls stopSniff
  let stopButton = createButton("Stop");
  stopButton.position(60, 10);
  stopButton.mousePressed(stopSniff);
}

function stopSniff() {
  sl.clear();
}

// Once the packets array has at least 5 packets, draw each packet
function draw() {
  if (packets.length > 5) {
    textSize(14);
    for (i = 0; i < 20; i++) {
      fill(0, 255, 255);
      text(packets[i], 0, i * 40 + 30);
    }
  }
}
```
