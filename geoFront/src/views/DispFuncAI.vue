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
              >系统当前采样结果</Button
            >
          </div>
        </dv-decoration7>
      </template>
      <!-- 脚本池区域 -->
      <CommonBlock
        v-for="(target, timestamp) in store.bindataList"
        :key="timestamp"
        :target="target"
        title="采集结果"
        operation="模型识别"
        name="名称"
        time="时间"
      >
      </CommonBlock>
    </ElCard>
    <ElCard>
      <!-- 头部区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button
              color="#615ea8"
              font-color="#615ea8"
              border="Border6"
              disabled="true"
              >识别结果</Button
            >
          </div>
        </dv-decoration7>
      </template>
      <!-- 脚本池区域 -->
      <AIResultBlock
        v-for="(target, timestamp) in store.resultList"
        :key="timestamp"
        :target="target"
      >
      </AIResultBlock>
    </ElCard>
  </div>
</template>

<script setup>
import CommonBlock from "./CommonBlock.vue";
import { useAIData } from "@/stores/ai";
import { Button } from "@kjgl77/datav-vue3";
import AIResultBlock from "./AIResultBlock.vue";

const store = useAIData();

const getAIInfo = () => {
  store.getAIInfo();
};
</script>
<style scoped src="../styles/dispbox.css"></style>
