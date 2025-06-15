<template>
  <div>
    <div class="func-show-container">
      <ElContainer>
        <ElMain>
          <ElRow>
            <ElCol>
              <ElButton
                class="show-button"
                color="rgba(20,20,20,0.8)"
                @click="onShowClick"
              >
                {{ command }}
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowEventClick"
              >
                事件
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowAIClick"
              >
                AI学习
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowWhiteListClick"
              >
                白名单
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowStaClick"
              >
                统计
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowDevClick"
              >
                设备管理
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowVerClick"
              >
                版本
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onShowUserClick"
              >
                账户设置
              </ElButton>
              <ElButton
                class="show-button"
                v-show="visible"
                color="rgba(20,20,20,0.8)"
                @click="onLogoutClick"
              >
                退出登陆
              </ElButton>
            </ElCol>
          </ElRow>
        </ElMain>
      </ElContainer>
    </div>
    <div class="func-container">
      <router-view v-if="visible"> </router-view>
    </div>
  </div>
</template>

<script>
import { ElCard, ElRow, ElCol, ElContainer, ElMain } from "element-plus";
export default {
  name: "DispFuncBox",
  components: {
    ElCard,
    ElRow,
    ElCol,
    ElContainer,
    ElMain,
  },
  data: () => ({
    command: "功能展开",
    visible: false,
  }),
  methods: {
    onShowClick() {
      if (this.visible) {
        this.command = "功能展开";
      } else {
        this.command = "功能折叠";
      }
      this.visible = !this.visible;
      this.$forceUpdate();
    },
    onShowEventClick() {
      this.$router.replace({ name: "FuncEvent" });
    },
    onShowAIClick() {
      this.$router.replace({ name: "FuncAI" });
    },
    onShowWhiteListClick() {
      this.$router.replace({ name: "FuncWhiLi" });
    },
    onShowStaClick() {
      this.$router.replace({ name: "FuncSta" });
    },
    onShowDevClick() {
      this.$router.replace({ name: "FuncDev" });
    },
    onShowVerClick() {
      this.$router.replace({ name: "FuncVer" });
    },
    onShowUserClick() {
      this.$router.replace({ name: "FuncUser" });
    },
    onLogoutClick() {
      this.$router.replace({ name: "LoginPage" });
    },
  },
};
</script>

<style scoped src="../styles/dispbox.css"></style>
