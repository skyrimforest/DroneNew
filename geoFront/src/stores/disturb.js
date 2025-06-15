import { defineStore } from "pinia";
import { doHttpRequest } from "@/modules/request";


export const useDisturbData = defineStore('disturb', {
    state: () => {  // 存放的就是模块的变量
        return {
            // 可用的指令
            command: "is a list",
            // 正在运行的脚本列表
            scriptList: {},
        }
    },
    getters: { // 相当于vue里面的计算属性，可以缓存数据

    },
    actions: { // 可以通过actions 方法，改变 state 里面的值。
        getCommandInfo() {
            doHttpRequest("GET_SCRIPT").then((res) => {
                this.command = res.data.config
            });
        },
    }
})


