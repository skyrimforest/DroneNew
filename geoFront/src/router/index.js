import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../components/GeoLoginPage.vue";
import MainPage from "../components/GeoMainPage.vue";
import DispFuncEvent from "../views/DispFuncEvent.vue";
import DispFuncAI from "../views/DispFuncAI.vue";
import DispFuncDev from "../views/DispFuncDev.vue";
import DispFuncSta from "../views/DispFuncSta.vue";
import DispFuncDis from "../views/DispFuncDis.vue";
import DispFuncTrap from "../views/DispFuncTrap.vue";
import DispFuncUser from "../views/DispFuncUser.vue";
import DispFuncVer from "../views/DispFuncVer.vue";
import DispFuncWhiLi from "../views/DispFuncWhiteList.vue";
import DispFuncPackDecode from "../views/DispFuncPackDecode.vue";
import DispFuncLLM from "../views/DispFuncLLM.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage,
    },
    {
      path: "/main",
      name: "MainPage",
      component: MainPage,
      children: [
        {
          path: "/main/event",
          name: "FuncEvent",
          component: DispFuncEvent,
        },
        {
          path: "/main/ai",
          name: "FuncAI",
          component: DispFuncAI,
        },
        {
          path: "/main/dev",
          name: "FuncDev",
          component: DispFuncDev,
        },
        {
          path: "/main/sta",
          name: "FuncSta",
          component: DispFuncSta,
        },
        {
          path: "/main/dis",
          name: "FuncDis",
          component: DispFuncDis,
        },
        {
          path: "/main/trap",
          name: "FuncTrap",
          component: DispFuncTrap,
        },
        {
          path: "/main/user",
          name: "FuncUser",
          component: DispFuncUser,
        },
        {
          path: "/main/ver",
          name: "FuncVer",
          component: DispFuncVer,
        },
        {
          path: "/main/whili",
          name: "FuncWhiLi",
          component: DispFuncWhiLi,
        },
        {
          path: "/main/decode",
          name: "FuncDecode",
          component: DispFuncPackDecode,
        },
        {
          path: "/main/llm",
          name: "FuncLLM",
          component: DispFuncLLM,
        },
      ],
    },
  ],
});

export default router;
