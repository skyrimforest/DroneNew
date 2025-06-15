import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/GeoLoginPage.vue'
import MainPage from '../components/GeoMainPage.vue'
import DispFuncEvent from '../views/DispFuncEvent.vue'
import DispFuncAI from '../views/DispFuncAI.vue'
import DispFuncDev from '../views/DispFuncDev.vue'
import DispFuncSta from '../views/DispFuncSta.vue'
import DispFuncDis from '../views/DispFuncDis.vue'
import DispFuncUser from '../views/DispFuncUser.vue'
import DispFuncVer from '../views/DispFuncVer.vue'
import DispFuncWhiLi from '../views/DispFuncWhiteList.vue'
import AIChildDrone from '../views/AIChildDrone.vue'
import AIChildSignal from '../views/AIChildSignal.vue'
import AIChildUniverse from '../views/AIChildUniverse.vue'
import AIChildUnknown from '../views/AIChildUnknown.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/main',
      name: 'MainPage',
      component: MainPage,
      children: [
        {
          path: '/main/event',
          name: "FuncEvent",
          component: DispFuncEvent,
        },
        {
          path: '/main/ai',
          name: "FuncAI",
          component: DispFuncAI,
          children: [
            {
              path: '/main/ai/drone',
              name: "AIDrone",
              component: AIChildDrone
            },
            {
              path: '/main/ai/signal',
              name: "AISig",
              component: AIChildSignal
            },
            {
              path: '/main/ai/universe',
              name: "AIUni",
              component: AIChildUniverse
            },
            {
              path: '/main/ai/unknown',
              name: "AIUnk",
              component: AIChildUnknown
            }
          ]
        },
        {
          path: '/main/dev',
          name: "FuncDev",
          component: DispFuncDev,
        },
        {
          path: '/main/sta',
          name: "FuncSta",
          component: DispFuncSta,
        },
        {
          path: '/main/dis',
          name: "FuncDis",
          component: DispFuncDis,
        },
        {
          path: '/main/user',
          name: "FuncUser",
          component: DispFuncUser,
        },
        {
          path: '/main/ver',
          name: "FuncVer",
          component: DispFuncVer,
        },
        {
          path: '/main/whili',
          name: "FuncWhiLi",
          component: DispFuncWhiLi,
        },

      ]
    },
  ]
})

export default router
