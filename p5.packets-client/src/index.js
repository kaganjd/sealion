// const url = "ws://127.0.0.1:8080/payload";
// const socket = new WebSocket(url);
// socket.onopen = () => socket.send("hey");
// socket.onmessage = event => console.log(`message: ${event.data}`);

function component() {
  let element = document.createElement("div");

  element.innerHTML = "Hello webpack";

  return element;
}

document.body.appendChild(component());
