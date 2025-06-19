<template>
  <div class="func-container">
    <dv-decoration7>
      <div color-white font-300>
        <Button
          color="#615ea8"
          font-color="#615ea8"
          border="Border6"
          @click="getAIInfo"
          >大模型接口</Button
        >
      </div>
    </dv-decoration7>
    <LLMChat> </LLMChat>
  </div>
</template>

<script setup>
import CommonBlock from "./CommonBlock.vue";
import { useAIData } from "@/stores/ai";
import { Button } from "@kjgl77/datav-vue3";
import AIResultBlock from "./AIResultBlock.vue";
import LLMChat from "./LLMChat.vue";
const store = useAIData();

const getAIInfo = () => {
  console.log("getAIInfo");
  store.getAIInfo();
};
</script>
<style scoped src="../styles/dispbox.css"></style>
