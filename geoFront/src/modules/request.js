import axios from "axios";
import APIS from "./api"


const service = axios.create({
    timeout: 15000,
})

// 这里api输入宏命名即可
const getApiUrl = (api) => {
    // 返回URL
    return [APIS[api][0], APIS[api][1]];
};

const getWsUrl = (api) => {
    return APIS[api];
}

const getSSEUrl = (api) => {
    return APIS[api][1];
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


const createSSE = (api, onMessage, onError) => {
    const eventSource = new EventSource(getSSEUrl(api));

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            onMessage && onMessage(data);
        } catch (e) {
            console.error("SSE 数据解析失败:", e, event.data);
        }
    };

    eventSource.onerror = (err) => {
        console.error("SSE 连接出错:", err);
        onError && onError(err);
    };

    return eventSource;
}

const showInfo = () => {
    console.log(APIS)
}

export {APIS, showInfo, doHttpRequest, createSSE, getWebSocket, getApiUrl}

