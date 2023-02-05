// server setup
const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
require("dotenv").config();

// server options
const app = express();
var options = {
  inflate: true,
  limit: "4000kb",
  type: "application/json",
};
app.use(bodyParser.raw(options));
app.use(express.static(path.join(__dirname, "build")));

const fetch = require("node-fetch-commonjs");
const WebSocket = require("ws");

const WS_CONNECTION = "wss://ws.tryterra.co/connect";

let hr_list = [];
let time_list = [];

//Generates a token for a developer
const generateToken = new Promise((resolve, reject) => {
  const options = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "dev-id": "emuc-dev-a10cjUlu33",
      "x-api-key": "ea4ca994c7b789eb188881e1e8c433ebd4f8c37c222eb31fc5e300d01e346a3c"
    }
  };

  return fetch("https://ws.tryterra.co/auth/developer", options)
    .then((response) => resolve(response.json()))
    .catch((err) => reject(console.error(err)));
});

function initWS(token) {
  const socket = new WebSocket(WS_CONNECTION);

  var expectingHeartBeatAck = false;

  socket.addEventListener("open", function (event) {
    console.log("Connection Established");
  });

  function heartBeat() {
    if (!expectingHeartBeatAck) {
      var heartBeatPayload = JSON.stringify({
        op: 0,
      });
      socket.send(heartBeatPayload);
      console.log("↑  " + heartBeatPayload);
      expectingHeartBeatAck = true;
    } else socket.close();
  }

  socket.addEventListener("message", function (event) {
    var message = JSON.parse(event.data);
    if (message["op"] == 2) {
      heartBeat();
      setInterval(heartBeat, message["d"]["heartbeat_interval"]);
      var payload = JSON.stringify(generatePayload(token));
      socket.send(payload);
      console.log("↑  " + payload);
    }
    if (message["op"] == 1) {
      expectingHeartBeatAck = false;
    }
    if (message["op"] == 5) {
      hr_list.push(message.d.val);
      console.log(message.d.val);
      time_list.push(message.d.ts);
    }
  });

  socket.addEventListener("close", function (event) {
    console.log("close");
    console.log(event.reason);
  });

  socket.addEventListener("error", function (event) {
    console.log("error");
    console.log(event);
  });
}

function generatePayload(token) {
  return {
    op: 3,
    d: {
      token: token,
      type: 1, //0  for user, 1 for developer
    },
  };
}

generateToken
  .then((tokenpayload) => {
    var token = tokenpayload["token"];
    initWS(token);
  })
  .catch((error) => {
    console.log(error);
  });

app.get("/api/hr", function (req, res) {
  const data = hr_list;
  res.status(200).json(data);
});

app.get("/api/timestamps", function (req, res) {
  const data = time_list;
  res.status(200).json(data);
});

// Server application
app.get("/*", function (req, res) {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

const port = "8888";
app.listen(port);
console.log("Server started on port " + port);
