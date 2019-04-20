---
id: api-open
title: open Method
sidebar_label: open
---
This method TK

## Usage
```js
open()
```
> Open the WebSocket connection.
### Parameters
None

### Example
```js
function setup() {
  createCanvas(400, 400);
  background(0);
  sl.socket.open()
    .then(() => sl.getNetworkInfo())
    .then(result => console.log(result))
    .then(() => sl.socket.close())
}
```
