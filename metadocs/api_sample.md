---
id: api-arpscan
title: arpScan Method
sidebar_label: arpScan
---

This method returns a Promise that resolves to an array of all active device's MAC addresses on the subnet with their corresponding IP addresses. Once the Promise has resolved, the array is available via the `arpTable` property.

```js
[
  {
    ipAddr: "192.168.0.38",
    mac: "14:22:db:99:6a:68"
  },
  {
    ipAddr: "192.168.0.64",
    mac: "0c:d7:46:65:3a:d9"
  }
];
```

## Usage

```js
arpScan(ipAddress);
```

> Scan the subnet of a given IP address to get a list of IP addresses and their corresponding MAC addresses

### Parameters

`ipAddress` _String_. A valid IP address on your subnet.

### Example

Once arpScan has resolved, the ARP table is available via the `arpTable` property:

```js
// Instantiate a SeaLion instance with hostname and port
const hostname = "localhost";
const port = 8080;
const sl = new SeaLion(hostname, port);

function setup() {
  createCanvas(400, 400);
  background(0);
  // Open the socket
  sl.socket
    .open()
    // Get network information
    .then(() => sl.getNetworkInfo())
    // Run arpScan using an IP address you get back form getNetworkInfo
    .then(networkResults => sl.arpScan(networkResults.gw))
    // Once arpScan has resolved, log the arpTable property
    .then(() => console.log(sl.arpTable));
}
```
