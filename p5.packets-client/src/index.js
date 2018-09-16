class Network {
  constructor(hostname, port) {
    this.hostname = hostname;
    this.port = port;
  }

  getInterface() {
    const url = "http://localhost:8080/interfaces";
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
