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
              <el-button @click="operationfunc"> {{ operation }} </el-button>
            </el-col>
          </el-row>
        </div>
      </template>

      <el-descriptions :column="1">
        <el-descriptions-item :label="name"
          ><el-tag>{{ target.filename }}</el-tag></el-descriptions-item
        >
        <el-descriptions-item :label="time"
          ><el-tag>{{ target.timestamp }}</el-tag></el-descriptions-item
        >
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { toRefs, onMounted, onUpdated } from "vue";

const props = defineProps({
  target: Object,
  title: String,
  operation: String,
  name: String,
  time: String,
  operationfunc: Function,
});
const { target, title, operation, name, time, operationfunc } = toRefs(props);

onMounted(() => {});
onUpdated(() => {});
</script>

<style scoped src="../styles/commonblock.css"></style>
