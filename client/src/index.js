import SeaLionSocket from './slsocket';

class SeaLion {
  constructor(hostname, port) {
    this.wsurl = `ws://${hostname}:${port}/sniff`
    this.socket = new SeaLionSocket(this.wsurl)
    this.arpTable = '';
    this.networkInfo = '';
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
    if (this.socket.readyState === 1) {
      this.socket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.socket.onmessage = event => {
        resolve(console.log(`${config.fname}: ${event.data}`));
      }
    });
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
    if (this.socket.readyState === 1) {
      this.validateIpAddress(ifaddrToSniff)
      this.socket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.socket.onmessage = event => {
        resolve(console.log(`${config.fname}: ${event.data}`));
      }
    });
  }

  // TODO: Move to a utils file
  validateIpAddress(ipAddress) {
    const periodCount = ipAddress.split('.').length -1
    if ( 7 <= ipAddress.length <= 15 && periodCount === 3) {
      return ipAddress
    } else {
      throw 'Error: The IP address you passed is not valid'
    }
  }

  arpScan(ifaddr) {
    const config = {
      fname: "arpScan",
      args: {
        ifaddr
      }
    };
    if (this.socket.readyState === 1) {
      this.validateIpAddress(ifaddr)
      this.socket.send(JSON.stringify(config));
    }
    return new Promise((resolve, reject) => {
      this.socket.onmessage = event => {
        this.arpTable = JSON.parse(event.data);
        resolve(this.arpTable)
      }
    });
  }

  getNetworkInfo() {
    const config = {
      fname: "getNetworkInfo"
    };
    if (this.socket.running === 1) {
      this.socket.send(JSON.stringify(config))
    }
    return new Promise((resolve, reject) => {
      this.socket.onmessage = event => {
        this.networkInfo = JSON.parse(event.data);
        resolve(this.networkInfo)
      }
    });
  }
}

console.log("SeaLion loaded!");
export default SeaLion;
