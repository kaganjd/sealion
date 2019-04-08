---
id: api-arpscan
title: arpScan Method
sidebar_label: arpScan
---
This method returns a Promise that resolves to an object of all active device's MAC addresses on the subnet with their corresponding IP addresses.

The object is in the form:

```js
{
  0: {
    "ipAddr": "192.168.0.38",
    "mac": "14:22:db:99:6a:68"
  },
  1: {
    "ipAddr": "192.168.0.64",
    "mac": "0c:d7:46:65:3a:d9"
  }
}
```

You can use getNetworkInfo() to get your IP address, pass it to arpScan() as an argument, and then access the returned table via the arpTable property.

# Method
arpScan(ipAddress)

Scans the subnet and returns an object of all active device's MAC addresses and corresponding IP addresses.

ipAddress: A valid IP address on your subnet.

# Example

```js

```
