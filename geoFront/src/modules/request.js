import axios from "axios";
import APIS from "./api"


const service = axios.create({
    timeout: 5000,
})

// 这里api输入宏命名即可
const getApiUrl = (api) => {
    // 返回URL
    return [APIS[api][0], APIS[api][1]];
};

const getWsUrl = (api) => {
    return APIS[api];
}

const doHttpRequest = (api, data) => {
    const [method, url] = getApiUrl(api);
    switch (method) {
        case "GET": {
            return service.get(url, data)
        }
        case "POST": {
            return service.post(url, data)
        }
    }
}

const getWebSocket = (api, data) => {
    const wsUrl = getWsUrl(api);
    let socket = new WebSocket(wsUrl);
    return socket;
}


const showInfo = () => {
    console.log(APIS)
}

export { APIS, showInfo, doHttpRequest, getWebSocket, getApiUrl }

