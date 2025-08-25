<template>
  <div>
    <ElCard>
      <!-- 头部区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button
              color="#615ea8"
              font-color="#615ea8"
              border="Border6"
              @click="getCommandInfo"
              >获取干扰命令</Button
            >
          </div>
        </dv-decoration7>
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
import DisturbBox from "./tools/DisturbBox.vue";
import ScriptBlock from "./tools/ScriptBlock.vue";
import { Button } from "@kjgl77/datav-vue3";

import { useDisturbData } from "@/stores/disturb";
const store = useDisturbData();

const getCommandInfo = () => {
  store.getCommandInfo();
};
</script>
<style scoped></style>
