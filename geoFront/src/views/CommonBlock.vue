<template>
  <div class="commonblock">
    <el-card>
      <!-- 头部区域 -->
      <template #header>
        <div class="card-header">
          <el-row>
            <el-col :span="12"
              ><el-tag>{{ title }}</el-tag>
            </el-col>
            <el-col :span="12">
              <el-button @click="closeSelf"> {{ operation }} </el-button>
            </el-col>
          </el-row>
        </div>
      </template>

      <el-descriptions :column="1">
        <el-descriptions-item :label="name"
          ><el-tag>{{ script.timestamp }}</el-tag></el-descriptions-item
        >
        <el-descriptions-item :label="time"
          ><el-tag>{{ script.command }}</el-tag></el-descriptions-item
        >
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, toRefs, onMounted, onUpdated, compile } from "vue";
import { doHttpRequest } from "@/modules/request";
import { useDisturbData } from "@/stores/disturb";
const store = useDisturbData();

const props = defineProps({
  target: Object,
  title: String,
  operation: String,
  name: String,
  time: String,
});
const { target, title, operation, name, time } = toRefs(props);

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
