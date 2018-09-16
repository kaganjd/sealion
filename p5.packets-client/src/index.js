class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
  }

  runSniffer() {
    this.socket = new WebSocket(`ws://${hostname}:${port}/sniffer`);
    this.socket.onopen = () => this.socket.send("message from client");
    this.socket.onmessage = event => console.log(`message: ${event.data}`);
  }

  getInterface() {
    const url = `http://${hostname}:${port}/interface`;
    let request = new XMLHttpRequest();
    request.open("GET", url);
    request.setRequestHeader("Content-Type", "application/json");
    request.send();

    request.onload = function(event) {
      console.log(request.response);
    };
  }
}

console.log("main.js loaded!");
module.exports = Network;
