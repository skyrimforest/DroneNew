import { defineStore } from "pinia";


export const useWebSocketData = defineStore('websocket', {
    state: () => {
        const wsUrl = "ws://192.168.0.123:10000";
        const socket = null;
        const initEventHandle = () => {
            socket.onopen = () => {
                console.log("WebSocket连接成功");
            };
            socket.onmessage = (msg) => {
                console.log("接收到消息:", msg);
            };
            socket.onerror = (error) => {
                console.error("WebSocket错误:", error);
            };
            socket.onclose = () => {
                console.log("WebSocket连接关闭");
            };
        };
        const createWebSocket = () => {
            socket = new WebSocket(wsUrl);
            initEventHandle();
        }
        return {
            allSocket: socket,
        }
    },
    getters: { // 相当于vue里面的计算属性，可以缓存数据

    },
    actions: { // 可以通过actions 方法，改变 state 里面的值。

    }
})


