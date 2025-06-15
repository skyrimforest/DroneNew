<template>
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
              功能展开
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              事件
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              AI学习
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              白名单
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              统计
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              设备管理
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              版本
            </ElButton>
            <ElButton
              class="show-button"
              v-show="visible"
              color="rgba(20,20,20,0.8)"
              @click="onShowClick"
            >
              账户设置
            </ElButton>
          </ElCol>
        </ElRow>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script>
import {
  ElIcon,
  ElHeader,
  ElContainer,
  ElMain,
  ElSelect,
  ElCol,
  ElRow,
  ElButton,
} from "element-plus";
export default {
  name: "DispFuncShowBox",
  components: {
    ElButton,
    ElContainer,
  },
  data: () => ({
    visible: false,
  }),
  methods: {
    onShowClick() {
        this.visible=!this.visible;
    },
  },
};
</script>
<style scoped src="../styles/dispbox.css"></style>