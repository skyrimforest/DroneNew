// 国际化,暂时只有首页作为示例

import { createI18n } from "vue-i18n";
import EN from "./en"
import CN from "./cn"

const message={
  zh:CN,
  en:EN,
}
const i18n = createI18n({
  legacy: false,//支持组合式api(vue3语法)
  globalInjection: true,//全局注册$t方法
  locale: navigator.language,
  messages: message
});

export default i18n