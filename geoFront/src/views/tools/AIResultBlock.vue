<template>
  <div class="airesultblock">
    <el-card>
      <!-- 头部区域 -->
      <template #header>
        <dv-loading v-if="target.loading">
          <div color-white>基本信息加载中...</div>
        </dv-loading>
        <div class="card-header">
          <el-row>
            <el-col :span="12"
              ><el-tag>{{ target.filename }}</el-tag>
            </el-col>
          </el-row>
        </div>
      </template>
      <dv-loading v-if="target.loading">
        <div color-white>推理结果加载中...</div>
      </dv-loading>
      <el-descriptions v-if="!target.loading">
        <el-descriptions-item label="推理结果">
          <el-image :src="target.url">
            <template #placeholder>
              <div class="image-slot">Loading<span class="dot">...</span></div>
            </template>
          </el-image>
        </el-descriptions-item>
        <el-descriptions-item label="类别"
          ><el-tag>{{ target.class }}</el-tag></el-descriptions-item
        >
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { toRefs, onMounted, onUpdated } from "vue";
const props = defineProps({
  target: Object,
});
const { target } = toRefs(props);

onMounted(() => {});
onUpdated(() => {});
</script>

<style scoped src="../../styles/airesultblock.css"></style>
