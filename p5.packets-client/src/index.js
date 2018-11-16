class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
    this.socket = new WebSocket(`ws://${hostname}:${port}/sniff`);
    this.socketStatus = this.translateReadyState(this.socket.readyState);
    this.running = 0;
    this.arpTable = "No ARP table yet";
    this.networkInfo = "No network info yet";
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

  sniffSelf(packetCount, iface = "", filter = "") {
    const config = {
      fname: "sniffSelf",
      args: {
        count: packetCount,
        iface: iface,
        filter: filter
      }
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event =>
      console.log(`${config.fname}: ${event.data}`);
  }

  stopSniffer() {
    const config = {
      fname: "stopSniffer"
    };
    if (this.socket.readyState === 1 && this.running === 1) {
      this.socket.send(JSON.stringify(config));
      this.socket.onclose = event => {
        this.running = 0;
        return this.running;
      };
    }
  }

  // TODO: add 'gateway' as a param?
  sniffNeighbor(packetCount, ifaddrToSniff) {
    const config = {
      fname: "sniffNeighbor",
      args: {
        count: packetCount,
        ifaddr: ifaddrToSniff
      }
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event =>
      console.log(`${config.fname}: ${event.data}`);
  }

  arpScan(ifaddr) {
    const config = {
      fname: "arpScan",
      args: {
        ifaddr
      }
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event => {
      this.arpTable = JSON.parse(event.data);
      return this.arpTable;
    };
  }

  getNetworkInfo() {
    const config = {
      fname: "getNetworkInfo"
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.socket.onmessage = event => {
      this.networkInfo = JSON.parse(event.data);
      return this.networkInfo;
    };
  }

  // async getInterface() {
  //   var url = `http://${hostname}:${port}/interface`;
  //   // https://fetch.spec.whatwg.org/#fetch-api
  //   let response = await fetch(url);
  //   return response.json();
  // }
}

console.log("main.js loaded");
module.exports = Network;
