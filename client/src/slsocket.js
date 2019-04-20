class SeaLionSocket extends WebSocket {
  constructor(url) {
    super(url)
    this.socketStatus = this.translateReadyState(this.readyState);
    this.running = 0;
  }
  
  open() {
    return new Promise((resolve, reject) => {
      this.onopen = () =>
        resolve(this.running = 1)
    })
  }

  close() {
    const config = {
      fname: "closeSocket"
    };
    this.send(JSON.stringify(config));
    this.onclose = event => {
      this.running = 0;
    };
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
}

export default SeaLionSocket;
