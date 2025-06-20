import { defineStore } from "pinia";
import { doHttpRequest } from "@/modules/request";

export const useDecoderData = defineStore("decode", {
  state: () => {
    // 存放的就是模块的变量
    return {
      // 已采集的二进制文件数据 需要filename和timestamp两个域
      bindataList: [],
      // loading filename class url
      resultList: [],
      loading: false,
    };
  },
  getters: {
    // 相当于vue里面的计算属性，可以缓存数据
  },
  actions: {
    // 可以通过actions 方法，改变 state 里面的值。
    getPacketInfo() {
      doHttpRequest("GET_PACKET").then((res) => {
        this.bindataList = res.data.filelist;
      });
    },
  },
});
