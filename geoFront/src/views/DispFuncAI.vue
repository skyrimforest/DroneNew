<template>
  <div class="func-container">
    <ElCard>
      <!-- 头部区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button
              color="#615ea8"
              font-color="#615ea8"
              border="Border6"
              @click="getAIInfo"
              >系统当前识别结果</Button
            >
          </div>
        </dv-decoration7>
      </template>
      <!-- 脚本池区域 -->
      <ScriptBlock
        v-for="(script, timestamp) in store.sampleList"
        :key="timestamp"
        :script="script"
      >
      </ScriptBlock>
    </ElCard>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import DisturbBox from "./DisturbBox.vue";
import ScriptBlock from "./ScriptBlock.vue";
import { useDisturbData } from "@/stores/disturb";
import { Button } from "@kjgl77/datav-vue3";

const store = useDisturbData();
const router = useRouter();

const getAIInfo = () => {
  console.log("getAIInfo");
};
</script>
<style scoped src="../styles/dispbox.css"></style>
