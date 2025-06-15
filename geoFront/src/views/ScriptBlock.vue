<template>
  <div class="scriptblock">
    <!-- "child pattern"{{ pattern }} -->
    <el-card>
      <!-- 头部区域 -->
      <template #header>
        <div class="card-header">
          <el-row>
            <el-col :span="12"><el-tag>脚本信息</el-tag> </el-col>
            <el-col :span="12">
              <el-button @click="closeSelf"> 关闭 </el-button>
            </el-col>
          </el-row>
        </div>
      </template>

      <el-descriptions :column="1">
        <el-descriptions-item label="UUID"
          ><el-tag>{{ script.timestamp }}</el-tag></el-descriptions-item
        >
        <el-descriptions-item label="Script"
          ><el-tag>{{ script.command }}</el-tag></el-descriptions-item
        >
      </el-descriptions>

      <!-- 主体区域 -->
      <!-- 脚部区域 -->
      <!-- <template #footer>Footer content</template> -->
    </el-card>
  </div>
</template>

<script setup>
import { ref, toRefs, onMounted, onUpdated, compile } from "vue";
import { doHttpRequest } from "@/modules/request";
import { useDisturbData } from "@/stores/disturb";
const store = useDisturbData();

const props = defineProps({
  script: Object,
});
const { script } = toRefs(props);

onMounted(() => {});
onUpdated(() => {});
const closeSelf = () => {
  const data = {
    uuid: script.value.timestamp,
  };
  doHttpRequest("STOP_SCRIPT", data)
    .then((res) => {
      delete store.scriptList[script.value.timestamp];
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped src="../styles/scriptblock.css"></style>
