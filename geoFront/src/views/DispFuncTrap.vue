<template>
  <div>
    <ElCard>
      <!-- 头部区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button
              color="#4d8dd9"
              font-color="#4d8dd9"
              border="Border6"
              @click="getDecoyCommand"
            >
              获取诱骗命令
            </Button>
          </div>
        </dv-decoration7>
      </template>

      <!-- 脚本池区域 -->
      <ScriptBlock
        v-for="(script, timestamp) in store.scriptList"
        :key="timestamp"
        :script="script"
      />
    </ElCard>

    <!-- 诱骗策略展示区域 -->
    <DecoyBox
      v-for="(pattern, key) in store.command.patterns"
      :key="key"
      :pattern="pattern.pattern"
    />
  </div>
</template>

<script setup>
import { Button } from "@kjgl77/datav-vue3";
import ScriptBlock from "./ScriptBlock.vue";
import DecoyBox from "./DecoyBox.vue";

import { useDecoyData } from "@/stores/decoy";
const store = useDecoyData();

const getDecoyCommand = () => {
  store.getDecoyCommand();
};
</script>
