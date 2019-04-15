---
id: api-sniffself
title: sniffSelf Method
sidebar_label: sniffSelf
---
This method TK

## Usage
```js
sniffSelf(packetCount, [iface], [filter])
```
> Capture packets sent to and from your own computer.

### Parameters
`packetCount` *Number.* How many packets to capture. Passing `0` sniffs an inifinite amount of packets.

`iface` *String (optional).* An interface to sniff. Defaults to scaPy's `conf.iface` on the server side if none is set.

`filter` *String (optional).* BPF filter to filter which packets you capture. See [http://biot.com/capstats/bpf.html](http://biot.com/capstats/bpf.html) for options.

### Example
```js
TK
```
