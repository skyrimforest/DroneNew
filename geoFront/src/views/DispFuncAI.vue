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
        :operationfunc="doInferReq(target)"
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
import { doHttpRequest } from "@/modules/request.js";
import APIS from "@/modules/api.js";

const store = useAIData();

const getAIInfo = () => {
  store.getAIInfo();
};

const doInferReq = (target) => {
  return () => {
    console.log("doInferReq");
    console.log(target);
    store.resultList.push({
      filename: target.filename,
      loading: true,
    });
    const idx = store.resultList.length - 1;
    const data = {
      info: {
        filename: target.filename,
      },
    };

    doHttpRequest("INFERREQ", data).then((res) => {
      console.log("res");
      console.log(res.data);
      store.resultList[idx] = res.data.infer;
      store.resultList[idx].url =
        APIS.GET_PIC[1] + "/" + res.data.infer.filename;
      store.resultList[idx].filename = target.filename;
      store.resultList[idx].loading = false;
      console.log(store.resultList[idx]);
    });
  };
};
</script>
<style scoped src="../styles/dispbox.css"></style>
