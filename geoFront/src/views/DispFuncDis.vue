<template>
  <div>
    <ElCard>
      <!-- 头部区域 -->
      <template #header>
        <ElButton @click="getCommandInfo">获取干扰命令</ElButton>
      </template>
      <!-- 脚本池区域 -->
      <ScriptBlock
        v-for="(script, timestamp) in store.scriptList"
        :key="timestamp"
        :script="script"
      >
      </ScriptBlock>
    </ElCard>
    <DisturbBox
      v-for="(pattern, key) in store.command.patterns"
      :key="key"
      :pattern="pattern.pattern"
    >
    </DisturbBox>
  </div>
</template>

<script setup>
import DisturbBox from "./DisturbBox.vue";
import { ref } from "vue";
import ScriptBlock from "./ScriptBlock.vue";

import { useDisturbData } from "@/stores/disturb";
const store = useDisturbData();

const getCommandInfo = () => {
  store.getCommandInfo();
};
</script>
<style scoped></style>
