<template>
  <div class="button-container">
    <ElRow>
      <ElButton class="custom-button" @click="testClick">
        地图模式切换
      </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 地图界面放大 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 地图界面缩小 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 返回防控区 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 矩形预警圈 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 六边形预警圈 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 圆形预警圈 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 擦除预警圈</ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 设置控制器坐标 </ElButton>
    </ElRow>
    <ElRow>
      <ElButton class="custom-button"> 返回中心点 </ElButton>
    </ElRow>
  </div>
</template>

<script>
import { ElButton, ElRow, ElCol } from "element-plus";
import axios from "axios";
import APIS from "@/modules/api.js";
export default {
  name: "DispMenuBox",
  components: {
    ElButton,
    ElCol,
    ElRow,
  },
  methods: {
    testClick() {
      const data = {
        user: "skyrim",
      };
      axios.post(APIS.blog, data).then((res) => {
        console.log(res);
      });
    },
  },
};
</script>


<style scoped>
.button-container {
  background-color: rgba(20, 20, 20, 0.8);
  backdrop-filter: blur(30px);
  border-radius: 10px;
}
.custom-button {
  width: 120px;
}
</style>
