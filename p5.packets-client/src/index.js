const url = "ws://127.0.0.1:8080/payload";
const socket = new WebSocket(url);

let element = document.createElement("div");

socket.onopen = () => socket.send("hey");

socket.onmessage = function(event) {
  element.innerHTML = `message: ${event.data}`;
  document.body.appendChild(element);
};
