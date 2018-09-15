class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
    this.socket = new WebSocket(`ws://${this.hostname}:${this.port}/payload`);
  }

  open() {
    this.socket.onopen = () => this.socket.send("hey");
  }

  monitor() {
    this.socket.onmessage = event => console.log(`message: ${event.data}`);
  }
}

console.log("main.js loaded!");
module.exports = Network;
