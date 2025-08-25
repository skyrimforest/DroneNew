<template>
  <div class="login-wrapper">
    <!-- <LoginBox /> -->
    <NewLoginBox />
  </div>
</template>

<script>
import { ElButton } from "element-plus";
import LoginBox from "../views/tools/LoginBox.vue";
import NewLoginBox from "../views/tools/NewLoginBox.vue";
import { showInfo, doHttpRequest } from "@/modules/request";

export default {
  name: "LoginPage",
  components: {
    ElButton,
    LoginBox,
    NewLoginBox
  },
  data: () => ({
    username: "",
    password: "",
  }),
  methods: {},
  mounted() {
    doHttpRequest("TEST");
  },
};
</script>

<style scoped>
/* 登录盒子容器，全屏居中 */
.login-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
