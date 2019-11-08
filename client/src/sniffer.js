import EventEmitter from "events";

class Sniffer extends WebSocket {
  constructor(url) {
    super(url);
    this.socketStatus = this.translateReadyState(this.readyState);
    this.running = 0;
    this.listener = new EventEmitter();
  }

  start(ip = false) {
    const sniffSelfConfig = {
      fname: "sniffSelf"
    };

    const sniffOtherConfig = {
      fname: "sniffNeighbor",
      args: {
        ifaddr: ip
      }
    };

    this.onopen = () => {
      ip === false
        ? this.send(JSON.stringify(sniffSelfConfig))
        : this.send(JSON.stringify(sniffOtherConfig));
    };

    this.onmessage = event => {
      console.log(event.data);
      this.listener.emit("packet", event.data);
    };
  }

  stop() {
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

export default Sniffer;
