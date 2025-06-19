const HTTP_PREFIX = "http";
const WS_PREFIX = "ws";
const DIS_URL_PREFIX = "://192.168.0.121:10002/";
const MAP_URL_PREFIX = "://192.168.0.121:9999/";
const MASTER_URL_PREFIX = "://192.168.0.121:10000/";
const OLLAMA_URL_PREFIX = "://localhost:11434/";


const ollamaApi = {
  GENERATE: ["POST", "api/generate"],
  CHAT: ["POST", "api/chat"],
};


const disApi = {
  TEST: ["POST", "script/"],
  RUN_SCRIPT: ["POST", "script/runscript"],
  STOP_SCRIPT: ["POST", "script/stopscript"],
  GET_SCRIPT: ["GET", "script/getscript"],
  DIS_HEARTBEAT: ["POST", "script/heartbeat"],
};

const mapApi = {
  LOGIN: ["POST", "api/login"],
  TEST: ["POST", "map/"],
  WHOLE: ["GET", "map/images/whole/{z}/{x}/{y}.jpg"],
  BEIJING: ["GET", "map/images/beijing/{z}/{x}/{y}.jpg"],
  SHANGHAI: ["GET", "map/images/shanghai/{z}/{x}/{y}.jpg"],
  GUANGZHOU: ["GET", "map/images/guangzhou/{z}/{x}/{y}.jpg"],
  SHENZHEN: ["GET", "map/images/shenzhen/{z}/{x}/{y}.jpg"],
  HARBIN: ["GET", "map/images/harbin/{z}/{x}/{y}.jpg"],
  MAP_HEARTBEAT: ["POST", "map/heartbeat"],
};

const masterApi = {
  FREQUENCY: ["GET", "zed/frequency"],
  UPDATE_MARKER: ["GET", "zed/marker"],
  FREQUENCY_CHILD: ["GET", "zed/frequency/child"],
  DRONE_PIC: ["GET", "zed/drone"],
  NODE_INFO: ["GET", "child/nodeinfo"],
  NODE_HEARTBEAT: ["POST", "child/heartbeat"],

  GET_BININFO: ["GET", "ai/getbininfo"],
  INFERREQ: ["POST", "ai/aipredict"],
  GET_PIC: ["GET", "ai/getpic"],

  GET_PACKET: ["GET", "decode/getpacketinfo"],
  DO_DECODE: ["POST", "decode/dodecode"],
};

const masterWebSocketApi = {
  MASTER_WEBSOCKET: "zed/ws/master",
  DRONE_WEBSOCKET: "zed/ws/drone",
};

for (const i in disApi) {
  disApi[i][1] = HTTP_PREFIX + DIS_URL_PREFIX + disApi[i][1];
}

for (const i in mapApi) {
  mapApi[i][1] = HTTP_PREFIX + MAP_URL_PREFIX + mapApi[i][1];
}

for (const i in masterApi) {
  masterApi[i][1] = HTTP_PREFIX + MASTER_URL_PREFIX + masterApi[i][1];
}
for (const i in ollamaApi) {
  ollamaApi[i][1] = HTTP_PREFIX + OLLAMA_URL_PREFIX + ollamaApi[i][1];
}
for (const i in masterWebSocketApi) {
  masterWebSocketApi[i] = WS_PREFIX + MASTER_URL_PREFIX + masterWebSocketApi[i];
}



const APIS = { ...disApi, ...mapApi, ...masterApi, ...masterWebSocketApi, ...ollamaApi };

export default APIS;
