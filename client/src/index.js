import Sniffer from "./sniffer";

class SeaLion {
  constructor(hostname, port) {
    this.baseUrl = `ws://${hostname}:${port}`;
    this.mainEndpoint = "/main";
    this.sniffEndpoint = "/sniff";
    this.sniffer = "";
    this.mainSocket = new WebSocket(`${this.baseUrl}${this.mainEndpoint}`);
    this.arpTable = "";
    this.networkInfo = "";
    this.packetList = "";
  }

  initSniffer(ip = false) {
    this.sniffer = new Sniffer(`${this.baseUrl}${this.sniffEndpoint}`);
    this.sniffer.start(ip);
  }

  clear() {
    this.mainSocket.close();
    if (this.sniffer) {
      this.sniffer.close();
    }
  }

  // TODO: Move to a utils file
  validateIpAddress(ipAddress) {
    const periodCount = ipAddress.split(".").length - 1;
    if (7 <= ipAddress.length <= 15 && periodCount === 3) {
      return ipAddress;
    } else {
      throw "Error: The IP address you passed is not valid";
    }
  }

  arpScan(ifaddr) {
    const config = {
      fname: "arpScan",
      args: {
        ifaddr
      }
    };
    if (this.mainSocket.readyState === 1) {
      this.validateIpAddress(ifaddr);
      this.mainSocket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.mainSocket.onmessage = event => {
        this.arpTable = JSON.parse(event.data);
        resolve(this.arpTable);
      };
    });
  }

  getNetworkInfo() {
    const config = {
      fname: "getNetworkInfo"
    };
    if (this.mainSocket.readyState === 1) {
      this.mainSocket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.mainSocket.onmessage = event => {
        this.networkInfo = JSON.parse(event.data);
        resolve(this.networkInfo);
      };
    });
  }
}

console.log("SeaLion loaded!");
export default SeaLion;
