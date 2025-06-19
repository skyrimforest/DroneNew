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
              @click="getPacketInfo"
              >采样报文</Button
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
              @click="getDecodeInfo"
            >
              解包数据查看
            </Button>
          </div>
        </dv-decoration7>
      </template>

      <!-- 解包展示区 -->
      <DecodeBlock
        v-for="(target, timestamp) in store.decodeList"
        :key="timestamp"
        :target="target"
        :title="`解包时间 ${timestamp}`"
      />
    </ElCard>
  </div>
</template>

<script setup>
import CommonBlock from "./CommonBlock.vue";
import { useAIData } from "@/stores/ai";
import { Button } from "@kjgl77/datav-vue3";
import AIResultBlock from "./AIResultBlock.vue";
import DecodeBlock from "./DecodeBlock.vue";
const store = useAIData();

const getPacketInfo = () => {
  console.log("getPacketInfo");
  store.getPacketInfo();
};
</script>
<style scoped src="../styles/dispbox.css"></style>
