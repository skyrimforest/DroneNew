import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";

// 引入pinia
import { createPinia } from "pinia";

//引入elementplus
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import "element-plus/theme-chalk/dark/css-vars.css";


//引入router
import router from "./router";

//引入i18n
import i18n from './i18n'

// 科技感UI
import DataVVue3 from '@kjgl77/datav-vue3'



const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(createPinia());
app.use(router);
app.use(ElementPlus);
app.use(i18n)
app.use(DataVVue3)

app.mount("#app");
