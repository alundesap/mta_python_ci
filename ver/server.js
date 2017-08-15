/*eslint no-console: 0*/
"use strict";

var http = require("http");
var port = process.env.PORT || 3000;

http.createServer(function (req, res) {
  res.writeHead(200, {"Content-Type": "text/plain"});
  res.end("Hello World\n NodeJS:" + process.version + "\nUpgrade with this: \nnpm cache clean -f\nnpm install -g n\nn " + process.version );
}).listen(port);

console.log("Server listening on port %d", port);
