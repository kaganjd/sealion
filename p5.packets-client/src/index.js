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

  runSniffer(count, filter, iface) {
    config = {
      count: count,
      filter: filter,
      iface: iface
    };
    this.socket.onopen = () => this.socket.send(JSON.stringify(config));
    this.running = 1;
    this.socket.onmessage = event =>
      console.log(`configSniffer: ${event.data}`);
  }

  stopSniffer() {
    if (this.socket.readyState === 1 && this.running === 1) {
      this.socket.send("stop");
      this.socket.onclose = event => (this.running = 0);
    }
  }

  getInterface() {
    const url = `http://${hostname}:${port}/interface`;
    let request = new XMLHttpRequest();
    request.open("GET", url);
    request.setRequestHeader("Content-Type", "application/json");
    request.send();

    request.onload = function(event) {
      console.log(`getInterface: ${request.response}`);
    };
  }
}

console.log("main.js loaded");
module.exports = Network;
