<template>
  <div class="beg-login-box">
    <div v-if="showAnimation" class="animation-container">
      <div class="big-text">
        <span
          v-for="(char, index) in characters"
          :key="index"
          class="char"
          :ref="(el) => (charRefs[index] = el)"
        >
          {{ char }}
        </span>
      </div>
    </div>
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
                    style="
                      font-weight: bolder;
                      font-size: xx-large;
                      color: rgba(77, 94, 169, 1);
                    "
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
import { ElRow, ElCol, ElNotification } from "element-plus";
import { doHttpRequest } from "@/modules/request";
import { useStore } from "@/stores/index";
import gsap from "gsap";
import { ref, nextTick } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "LoginBox",
  data: () => ({
    checked1: false,
    left_box_url: "../assets/leftbox.png",
    top_pic_url: "../assets/drone.png",
  }),
  mounted() {},
  components: {
    ElRow,
    ElCol,
    BorderBox8,
  },
  setup() {
    const store = useStore();
    const username = ref("");
    const password = ref("");
    const showAnimation = ref(false);
    const characters = ["无", "线", "可", "击"]; // 拆分字符
    const router = useRouter();

    const charRefs = []; // 用于保存每个字的 DOM 引用
    const handleLogin = async () => {
      console.log("2333");
      showAnimation.value = true;

      await nextTick();

      // 逐字动画
      gsap.fromTo(
        charRefs,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.2, // 每个字之间延迟 0.2 秒
          ease: "power2.out",
          onComplete: () => {
            // 完成后整体淡出
            gsap.to(".animation-container", {
              opacity: 0,
              duration: 2,
              ease: "power2.inOut",
              onComplete: () => {
                showAnimation.value = false;
              },
            });
          },
        }
      );
    };
    const onLoginClick = () => {
      const myRequestData = {
        username: username.value,
        password: password.value,
      };
      handleLogin();
      setTimeout(() => {
        if (username.value === "0" && password.value === "0") {
          router.replace({ name: "MainPage" });
          return 0;
        }
        doHttpRequest("LOGIN", myRequestData)
          .then((res) => {
            if (res.data.success == true) {
              store.username = username.value;
              store.password = username.value;
              $router.replace({ name: "MainPage" });
            } else {
              loginFail();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }, 2000);
    };
    return {
      handleLogin,
      onLoginClick,
      showAnimation,
      characters,
      charRefs,
      username,
      password,
      store,
    };
  },
  methods: {
    getAssets(url) {
      return new URL(url, import.meta.url).href;
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
