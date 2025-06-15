// 全局事件总线用于兄弟间传递数据

import mitt from "mitt";

const emitter = mitt();

export default emitter;
