class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
    this.socket = new WebSocket(`ws://${hostname}:${port}/sniffer`);
    this.socketStatus = this.translateReadyState(this.socket.readyState);
    this.running = 0;
  }

  translateReadyState(readyState) {
    if (readyState === 0) {
      return "CONNECTING";
    } else if (readyState === 1) {
      return "OPEN";
    } else if (readyState === 2) {
      return "CLOSING";
    } else if (readyState === 3) {
      return "CLOSED";
    }
  }

  // TODO: Make iface optional arg; remove filter?
  sniffSelf(iface, packetCount, filter) {
    const config = {
      count: packetCount,
      filter: filter,
      iface: iface
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event => console.log(`sniffSelf: ${event.data}`);
  }

  stopSniffer() {
    if (this.socket.readyState === 1 && this.running === 1) {
      this.socket.send("stop");
      this.socket.onclose = event => (this.running = 0);
    }
  }

  // TODO: Make iface optional arg
  sniffNeighbor(ifaddr, packetCount) {
    const config = {
      ifaddr: ifaddr,
      count: packetCount
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event =>
      console.log(`sniffNeighbor: ${event.data}`);
  }

  async arpScan(ifaddr) {
    // https://fetch.spec.whatwg.org/#fetch-api
    var url = new URL(`http://${hostname}:${port}/arp`),
      params = { ifaddr: ifaddr };
    Object.keys(params).forEach(key =>
      url.searchParams.append(key, params[key])
    );
    let response = await fetch(url);
    return response.json();
  }

  async getInterface() {
    var url = `http://${hostname}:${port}/interface`;
    let response = await fetch(url);
    return response.json();
  }
}

console.log("main.js loaded");
module.exports = Network;
