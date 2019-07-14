import Sniffer from "./sniffer";

class SeaLion {
  constructor(hostname, port) {
    this.wsSniff = `ws://${hostname}:${port}/sniff`;
    this.wsMain = `ws://${hostname}:${port}/main`;
    this.sniffer = new Sniffer(this.wsSniff);
    this.mainSocket = new WebSocket(this.wsMain);
    this.arpTable = "";
    this.networkInfo = "";
    this.packetList = "";
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
    if (this.mainSocket.running === 1) {
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
