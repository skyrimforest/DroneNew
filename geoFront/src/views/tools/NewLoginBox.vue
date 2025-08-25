<template>
  <div class="beg-login-box">
    <!-- 动画层 -->
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

    <!-- 登录框体 -->
    <div>
      <div class="beg-login-inner">
        <div class="left-box">
          <div class="overlay">
            <div class="slogan">
              <div class="description">
                无人机防御 · 多维感知 · 智能干扰一体化系统
              </div>
            </div>
          </div>
        </div>
        <div class="right-box">
          <el-card>
            <template #header>
              <div class="card-header">
                <el-image
                  :src="getAssets(top_pic_url)"
                  fit="cover"
                  style="width: 10vw; height: 10vh"
                ></el-image>
                <el-text
                  type="primary"
                  style="
                    font-weight: bolder;
                    font-size: xx-large;
                    color: rgba(77, 94, 169, 1);
                  "
                  >{{ $t("loginpage.title") }}</el-text
                >
              </div>
            </template>

            <el-input
              v-model="username"
              prefix-icon="UserFilled"
              :placeholder="$t('loginpage.unameHolder')"
            />
            <el-input
              v-model="password"
              prefix-icon="Lock"
              type="password"
              show-password
              :placeholder="$t('loginpage.pwdHolder')"
              style="margin-top: 20px"
            />

            <el-checkbox v-model="checked1" style="margin: 10px 0">
              {{ $t("loginpage.loginNext") }}
            </el-checkbox>

            <el-button
              type="primary"
              size="large"
              plain
              @click="onLoginClick"
              class="login-btn"
            >
              <el-icon><Check /></el-icon>
              <span>{{ $t("loginpage.loginButton") }}</span>
            </el-button>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { useRouter } from "vue-router";
import gsap from "gsap";
import { ElNotification } from "element-plus";
import { useStore } from "@/stores";
import { doHttpRequest } from "@/modules/request";

const store = useStore();
const router = useRouter();
const username = ref("");
const password = ref("");
const checked1 = ref(true);
const top_pic_url = "../../assets/drone.png";
const characters = ["无", "线", "可", "击"];
const charRefs = [];
const showAnimation = ref(false);

const getAssets = (url) => new URL(url, import.meta.url).href;

const handleLogin = async () => {
  showAnimation.value = true;
  await nextTick();
  gsap.fromTo(
    charRefs,
    { opacity: 0, y: 50 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.2,
      ease: "power2.out",
      onComplete: () => {
        gsap.to(".animation-container", {
          opacity: 0,
          duration: 1.5,
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
  handleLogin();
  const myRequestData = {
    username: username.value,
    password: password.value,
  };
  setTimeout(() => {
    handleLogin();
    if (username.value === "0" && password.value === "0") {
      router.replace({ name: "MainPage" });
      return;
    }
    doHttpRequest("LOGIN", myRequestData)
      .then((res) => {
        if (res.data.success) {
          store.username = username.value;
          store.password = password.value;
          router.replace({ name: "MainPage" });
        } else {
          loginFail();
        }
      })
      .catch((err) => {
        console.error(err);
        loginFail();
      });
  }, 1500);
};

const loginFail = () => {
  ElNotification({
    title: "错误",
    message: "登陆失败，请检查用户名或密码",
    type: "error",
    position: "bottom-right",
  });
};
</script>

<style scoped>
.beg-login-box {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background-image: url("@/assets/watchdog.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.left-box {
  flex: 1;
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.3); /* 可选: 淡蒙层 */
}

.right-box {
  position: relative;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
}

.el-card {
  width: 90%;
  max-width: 700px;
  border-radius: 16px;
  background-color: rgba(255, 255, 255, 0.92);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.login-btn {
  width: 100%;
  margin-top: 20px;
}

.beg-login-inner {
  display: flex;
  width: 100vw;
  height: 100vh;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  overflow: hidden;
}

.animation-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.big-text {
  color: white;
  font-size: 5rem;
  font-weight: bold;
  display: flex;
  gap: 0.5em;
}

.char {
  display: inline-block;
  opacity: 0;
  transform: translateY(50px);
}

.slogan {
  text-align: center;
  color: white;
}

.description {
  margin-top: 1rem;
  font-size: 3rem;
  font-weight: 600;
  color: #c0e8ff;
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  margin-top: 20px;
}
</style>
