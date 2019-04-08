class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
    this.socket = new WebSocket(`ws://${hostname}:${port}/sniff`);
    this.socketStatus = this.translateReadyState(this.socket.readyState);
    this.running = 0;
    this.arpTable = '';
    this.networkInfo = '';
  }

  //TODO: Add socketHandler method to set up, shut down, and maintain this.running instead of having this.socket.onopen in every method
  // socketHandler() {
  // }

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
    return new Promise((resolve, reject) => {
      if (this.socket.readyState === 1) {
        this.socket.send(JSON.stringify(config));
      }
      this.socket.onmessage = event =>
        resolve(console.log(`${config.fname}: ${event.data}`));
    });
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
    return new Promise((resolve, reject) => {
      if (this.socket.readyState === 1) {
        this.socket.send(JSON.stringify(config));
      }
      this.socket.onmessage = event =>
        resolve(console.log(`${config.fname}: ${event.data}`));
    })
  }

  arpScan(ifaddr) {
    const config = {
      fname: "arpScan",
      args: {
        ifaddr
      }
    };
    return new Promise((resolve, reject) => {
      if (this.socket.readyState === 1) {
        this.socket.send(JSON.stringify(config));
      }
      this.socket.onmessage = event => {
        this.arpTable = JSON.parse(event.data);
        resolve(this.arpTable)
      }
    });
  }

  getNetworkInfo() {
    const config = {
      fname: "getNetworkInfo"
    };
    return new Promise((resolve, reject) => {
      this.socket.onopen = () => this.socket.send(JSON.stringify(config));
      this.socket.onmessage = event => {
        this.networkInfo = JSON.parse(event.data);
        resolve(this.networkInfo)
      }
    });
  }
}

console.log("main.js loaded");
module.exports = Network;
