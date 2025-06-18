<template>
  <div class="common-layout">
    <Draggable></Draggable>
    <ElContainer class="layout-container">
      <!-- 顶部上框线 -->
      <ElHeader class="top-header">
        <dv-border-box12 class="logo-area">
          <img
            :src="getAssets('../assets/logo.png')"
            alt="Logo"
            class="logo-img"
          />
          <div class="logo-title">察打一体无人机防御系统</div>
        </dv-border-box12>
      </ElHeader>
      <ElContainer>
        <ElAside class="sidebar">
          <dv-border-box12 class="border-box-wrapper">
            <ElMenu
              class="custom-menu"
              background-color="#1e1e2f"
              text-color="#e0e0e0"
              active-text-color="#00ffc6"
              :collapse="false"
            >
              <ElSubMenu index="1">
                <template #title>
                  <Button fontColor="#E6F7FF" class="menu-button" plain>
                    <el-icon><MapLocation /></el-icon>
                    地图控制
                  </Button>
                </template>
                <ElMenuItemGroup>
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="zoomIn"
                    >地图放大</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="zoomOut"
                    >地图缩小</Button
                  >
                </ElMenuItemGroup>
              </ElSubMenu>

              <ElSubMenu index="2">
                <template #title>
                  <Button fontColor="#E6F7FF" class="menu-button" plain>
                    <el-icon><EditPen /></el-icon>
                    预警区绘制
                  </Button>
                </template>
                <ElMenuItemGroup>
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="drawRect"
                    >矩形预警区</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="drawCir"
                    >圆形预警区</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="drawRemove"
                    >擦除预警区</Button
                  >
                </ElMenuItemGroup>
              </ElSubMenu>

              <ElSubMenu index="3">
                <template #title>
                  <Button fontColor="#E6F7FF" class="menu-button" plain>
                    <el-icon><Link /></el-icon>
                    控制区控制
                  </Button>
                </template>
                <ElMenuItemGroup>
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="drawMarker"
                    >设置控制区坐标</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="centerReturn"
                    >返回中心点</Button
                  >
                </ElMenuItemGroup>
              </ElSubMenu>

              <ElSubMenu index="4">
                <template #title>
                  <Button fontColor="#E6F7FF" class="menu-button" plain>
                    <el-icon><Setting /></el-icon>
                    反击功能展开
                  </Button>
                </template>
                <ElMenuItemGroup>
                  <!-- <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2event"
                    >事件展示</Button
                  > -->
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2llm"
                    >智能体助理</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2ai"
                    >AI学习</Button
                  >
                  <!-- <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2white"
                    >报文解密</Button
                  > -->
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2decode"
                    >报文解密</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2statis"
                    >统计</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2disturb"
                    >干扰</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2device"
                    >设备管理</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2version"
                    >版本管理</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2user"
                    >账户管理</Button
                  >
                  <Button
                    color="#00ffc6"
                    class="menu-action-button"
                    @click="jump2logout"
                    >退出登录</Button
                  >
                </ElMenuItemGroup>
              </ElSubMenu>
            </ElMenu></dv-border-box12
          >
        </ElAside>
        <ElMain>
          <NewMapContainer></NewMapContainer>
        </ElMain>
      </ElContainer>
    </ElContainer>
    <ElDrawer v-model="drawer" size="50%">
      <template #header>
        <h4>{{ command }}</h4>
      </template>
      <template #default>
        <div class="draw-box">
          <router-view> </router-view>
        </div>
      </template>
      <template #footer> </template>
    </ElDrawer>
  </div>
</template>

<script setup>
// 地图选型
import NewMapContainer from "../views/NewMapComTrans.vue";
import Draggable from "../views/Draggable.vue";

import { ref, onMounted } from "vue";

import { Button } from "@kjgl77/datav-vue3";

// 引入路由
import { useRouter } from "vue-router";
const router = useRouter();

// 引入全局管理
import { useMapDataStore } from "../stores/mapData";
import { useMusicData } from "../stores/music";
const store = useMapDataStore();
const musicStore = useMusicData();

const getAssets = (url) => {
  return new URL(url, import.meta.url).href;
};

// ----------音乐播放代码----------
onMounted(() => {
  musicStore.playMusic("BGM");
});

// ----------地图控制区域代码----------
// 地图变大
const zoomIn = () => {
  store.zoomIn();
};

// 地图缩小
const zoomOut = () => {
  store.zoomOut();
};

// ----------预警区绘制区域代码----------
const drawRect = () => {
  store.drawRect();
};
const drawCir = () => {
  store.drawCir();
};
const drawRemove = () => {
  store.drawRemove();
};

// ----------控制区控制区域代码----------
const drawMarker = () => {
  store.drawMarker();
};
const centerReturn = () => {
  store.centerReturn();
};

// ----------draw控件展示代码----------
const drawer = ref(0);
const command = ref("no command");

const jump2event = () => {
  drawer.value = 1;
  command.value = "事件展示";
  router.replace({ name: "FuncEvent" });
};
const jump2ai = () => {
  drawer.value = 1;
  command.value = "AI学习";
  router.replace({ name: "FuncAI" });
};
const jump2llm = () => {
  drawer.value = 1;
  command.value = "智能体助理";
  router.replace({ name: "FuncLLM" });
};
const jump2white = () => {
  drawer.value = 1;
  command.value = "白名单";
  router.replace({ name: "FuncWhiLi" });
};
const jump2decode = () => {
  drawer.value = 1;
  command.value = "报文解密";
  router.replace({ name: "FuncDecode" });
};
const jump2statis = () => {
  drawer.value = 1;
  command.value = "统计";
  router.replace({ name: "FuncSta" });
};
const jump2disturb = () => {
  drawer.value = 1;
  command.value = "干扰";
  router.replace({ name: "FuncDis" });
};
const jump2device = () => {
  drawer.value = 1;
  command.value = "设备管理";
  router.replace({ name: "FuncDev" });
};
const jump2version = () => {
  drawer.value = 1;
  command.value = "版本管理";
  router.replace({ name: "FuncVer" });
};
const jump2user = () => {
  drawer.value = 1;
  command.value = "账户管理";
  router.replace({ name: "FuncUser" });
};
const jump2logout = () => {
  drawer.value = 1;
  command.value = "事件展示";
  router.replace({ name: "LoginPage" });
};
</script>

<style src="../styles/mainpage.css" scoped></style>
