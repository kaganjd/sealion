import SeaLionSocket from "./slsocket";

class SeaLion {
  constructor(hostname, port) {
    this.wsSniff = `ws://${hostname}:${port}/sniff`;
    this.wsMain = `ws://${hostname}:${port}/main`;
    this.sniffSocket = new SeaLionSocket(this.wsSniff);
    this.mainSocket = new SeaLionSocket(this.wsMain);
    this.arpTable = "";
    this.networkInfo = "";
    this.packetList = "";
  }

  sniffSelf(packetCount, iface = "", filter = "") {
    const config = {
      fname: "sniffSelf",
      args: {
        count: packetCount,
        iface: iface,
        filter: filter
      }
    };
    const packetArray = [];

    if (this.sniffSocket.readyState === 1) {
      this.sniffSocket.send(JSON.stringify(config));
    }

    this.sniffSocket.onmessage = event => {
      packetArray.push(event.data);
      // if (packetArray.length == config.args.count) {
      return new Promise((resolve, reject) => {
        this.packetList = packetArray;
        resolve(this.packetList);
      });
      // }
    };
  }

  // TODO: add 'gateway' as a param?
  sniffNeighbor(packetCount, ifaddrToSniff) {
    const config = {
      fname: "sniffNeighbor",
      args: {
        count: packetCount,
        ifaddr: ifaddrToSniff
      }
    };
    if (this.sniffSocket.readyState === 1) {
      this.validateIpAddress(ifaddrToSniff);
      this.sniffSocket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.sniffSocket.onmessage = event => {
        resolve(console.log(`${config.fname}: ${event.data}`));
      };
    });
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
