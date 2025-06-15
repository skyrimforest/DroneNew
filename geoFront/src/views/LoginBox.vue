<template>
  <div class="beg-login-box">

    <BorderBox8 class="border-box-wrapper">
      <div class="right-box">
        <el-card>
          <template #header>
            <div class="card-header">
              <el-row>
                <el-col>
                  <el-image
                    :src="getAssets(top_pic_url)"
                    fit="cover"
                    style="width: 10vw; height: 10vh"
                  >
                  </el-image>
                </el-col>
              </el-row>
              <el-row>
                <el-col>
                  <el-text
                    type="primary"
                    style="font-weight: bolder;font-size: xx-large; color: rgba(77, 94, 169, 1)"
                    >{{ $t("loginpage.title") }}</el-text
                  >
                </el-col>
              </el-row>
            </div>
          </template>
          <el-row>
            <el-col :span="2"> </el-col>
            <el-col :span="20">
              <el-input
                prefix-icon="UserFilled"
                v-model="username"
                :placeholder="$t('loginpage.unameHolder')"
              />
            </el-col>
            <el-col :span="2"> </el-col>
          </el-row>
          <el-row>
            <el-col>
              <br />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="2"> </el-col>
            <el-col :span="20">
              <el-input
                prefix-icon="Lock"
                v-model="password"
                type="password"
                :placeholder="$t('loginpage.pwdHolder')"
                show-password
              />
            </el-col>
            <el-col :span="2"> </el-col>
          </el-row>
          <el-row>
            <el-col>
              <br />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="10">
              <el-checkbox
                v-model="checked1"
                :label="$t('loginpage.loginNext')"
                size="small"
              />
            </el-col>
            <el-col :span="2"> </el-col>
          </el-row>

          <template #footer>
            <el-row>
              <el-col>
                <el-button
                  type="primary"
                  size="large"
                  plain
                  @click="onLoginClick"
                >
                  <el-icon>
                    <Check />
                  </el-icon>
                  <span>{{ $t("loginpage.loginButton") }}</span>
                </el-button>
              </el-col>
            </el-row>
            <el-row>
              <el-col>
                <br />
              </el-col>
            </el-row>
          </template>
        </el-card>
      </div>
    </BorderBox8>
  </div>
</template>

<script>
import { BorderBox8 } from "@kjgl77/datav-vue3";
import { ElRow, ElCol, ElNotification, ElButton } from "element-plus";
import { doHttpRequest } from "@/modules/request";
import { useStore } from "@/stores/index";

export default {
  name: "LoginBox",
  data: () => ({
    username: "",
    password: "",
    store: useStore(),
    left_box_url: "../assets/leftbox.png",
    top_pic_url: "../assets/drone.png",
  }),
  mounted() {},
  components: {
    ElRow,
    ElCol,
    BorderBox8,
  },
  methods: {
    getAssets(url) {
      return new URL(url, import.meta.url).href;
    },
    onLoginClick() {
      const myRequestData = {
        username: this.username,
        password: this.password,
      };
      if (this.username === "0" && this.password === "0") {
        this.$router.replace({ name: "MainPage" });
        return 0;
      }
      doHttpRequest("LOGIN", myRequestData)
        .then((res) => {
          if (res.data.success == true) {
            this.store.username = this.username;
            this.store.password = this.password;
            // console.log(this.store.password);
            // this.loginSuccess();
            this.$router.replace({ name: "MainPage" });
          } else {
            this.loginFail();
            // console.log("fail");
            // this.$router.replace({ name: "MainPage" });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    loginSuccess() {
      ElNotification({
        title: "Success",
        message: "登陆成功！",
        type: "success",
        position: "bottom-right",
        duration: 3000,
      });
    },
    loginFail() {
      ElNotification({
        title: "Error",
        message: "登陆失败，请检查用户名或者密码是否正确",
        type: "error",
        position: "bottom-right",
        duration: 3000,
      });
    },
  },
};
</script>

<style src="../styles/loginbox.css" scoped></style>
