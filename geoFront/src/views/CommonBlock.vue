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
              <el-button @click="doInferReq"> {{ operation }} </el-button>
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
import { ref, toRefs, onMounted, onUpdated } from "vue";
import { useAIData } from "@/stores/ai";
import { APIS } from "@/modules/request";
import { doHttpRequest, getWebSocket } from "@/modules/request.js";

const store = useAIData();

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

const doInferReq = () => {
  console.log("doInferReq");
  console.log(target);
  console.log(target.value);
  store.resultList.push({
    filename: target.value.filename,
    loading: true,
  });
  const idx = store.resultList.length - 1;
  const data = {
    info: {
      filename: target.value.filename,
    },
  };

  doHttpRequest("INFERREQ", data).then((res) => {
    console.log("res");
    console.log(res.data);
    store.resultList[idx] = res.data.infer;
    store.resultList[idx].url = APIS.GET_PIC[1] +'/'+ res.data.infer.filename;
    store.resultList[idx].loading = false;
    console.log(store.resultList[idx]);
  });
};
</script>

<style scoped src="../styles/commonblock.css"></style>
