<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <el-menu :default-active="1" mode="horizontal">
          <el-menu-item index="1" @click="jump2drone">未知Wifi无人机名单</el-menu-item>
          <el-menu-item index="2" @click="jump2signal">信号学习</el-menu-item>
          <el-menu-item index="3" @click="jump2universe">通用检测器</el-menu-item>
          <el-menu-item index="4" @click="jump2unknown">未知信号</el-menu-item>
        </el-menu>
      </ElHeader>
      <ElMain style="--el-main-padding: 0px">
        <ElScrollbar>
          <router-view>
          </router-view>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>



<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const droneData = [
  {
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
];
function jump2drone() {
  router.push({ name: "AIDrone" })

}
function jump2signal() {
  router.push({ name: "AISig" })

}
function jump2universe() {
  router.push({ name: "AIUni" })

}
function jump2unknown() {
  router.push({ name: "AIUnk" })

}
</script>
<style scoped src="../styles/dispbox.css"></style>