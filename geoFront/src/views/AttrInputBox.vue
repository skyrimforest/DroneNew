<template>
  <ElDialog
    v-model="dialogVisible"
    title="无人机属性设置"
    width="30%"
    :before-close="handleClose"
  >
    <ElRow>
      <ElCol :span="6"> 无人机类型 </ElCol>
      <ElCol :span="18">
        <ElInput prefix-icon="UserFilled" v-model="username"> </ElInput>
      </ElCol>
    </ElRow>
    <ElRow>
      <ElCol :span="6"> 无人机关联ID </ElCol>
      <ElCol :span="18">
        <ElInput prefix-icon="UserFilled" v-model="username"> </ElInput>
      </ElCol>
    </ElRow>
    <ElRow>
      <ElCol :span="6"> 详细描述 </ElCol>
      <ElCol :span="18">
        <ElInput prefix-icon="UserFilled" v-model="username"> </ElInput>
      </ElCol>
    </ElRow>
    <ElRow style="margin-top: 30px; font-size: small">
      <ElCol> 删除属性：保持上面所有字段为空，并选择“确定”按钮 </ElCol>
    </ElRow>
    <template #footer>
      <span class="dialog-footer">
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton type="primary" @click="dialogVisible = false">
          确认
        </ElButton>
      </span>
    </template>
  </ElDialog>
</template>

<script>
import { ElRow, ElCol, ElDialog, ElButton, ElInput } from "element-plus";
import axios from "axios";
import APIS from "@/modules/api";
import { doHttpRequest } from "@/modules/request";
import { useStore } from "@/stores/index";

export default {
  name: "AttrInputBox",
  data: () => ({
    store: useStore,
    dialogVisible: false,
  }),
  mounted() {},
  created() {},
  components: {
    ElRow,
    ElCol,
    ElDialog,
    ElButton,
    ElInput,
  },
  methods: {
    onLoginClick() {
      const myRequestData = {
        username: this.username,
        password: this.password,
      };
      doHttpRequest("LOGIN", myRequestData).then((res) => {
        this.msta = "success";
        console.log(res);
      });
      this.$router.replace({ name: "MainPage" });
    },
  },
};
</script>

<style scoped>
.beg-login-box {
  text-align: center;

  width: 450px;
  height: 200px;
  margin: 10% auto;
  background-color: rgba(127, 127, 127, 0.5);
  border-radius: 10px;
}
</style>
