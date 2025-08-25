<template>
  <div class="func-container">
    <ElCard>
      <!-- 报文采样区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button
                color="#615ea8"
                font-color="#615ea8"
                border="Border6"
                @click="getPacketInfo"
            >采样报文
            </Button
            >
          </div>
        </dv-decoration7>
      </template>
      <!-- 报文信息展示区域 -->
      <CommonBlock
          v-for="(target, timestamp) in store.bindataList"
          :key="timestamp"
          :target="target"
          title="采集结果"
          operation="解码报文"
          name="名称"
          time="时间"
          :operationfunc="doDecodeReq(target)"
      >
      </CommonBlock>
    </ElCard>
    <ElCard>
      <!-- 解包数据指令区域 -->
      <template #header>
        <dv-decoration7>
          <div color-white font-300>
            <Button color="#615ea8" font-color="#615ea8" border="Border6">
              解包数据查看
            </Button>
          </div>
        </dv-decoration7>
      </template>

      <!-- 解包数据展示区 -->
      <DecodeBlock
          v-for="(target, timestamp) in store.resultList"
          :key="timestamp"
          :target="target"
          :title="`解包时间 ${timestamp}`"
      />
    </ElCard>
  </div>
</template>

<script setup>
import CommonBlock from "./tools/CommonBlock.vue";
import {Button} from "@kjgl77/datav-vue3";
import DecodeBlock from "./tools/DecodeBlock.vue";
import {useDecoderData} from "@/stores/decoder";
import {doHttpRequest} from "@/modules/request.js";
import APIS from "@/modules/api.js";

const store = useDecoderData();

const getPacketInfo = () => {
  console.log("getPacketInfo");
  console.log(APIS)
  store.getPacketInfo();
};

const doDecodeReq = (target) => {
  return () => {
    console.log(target);
    store.resultList.push({
      filename: target.filename,
      loading: true,
    });
    console.log(store.resultList);
    const idx = store.resultList.length - 1;
    const data = {
      info: {
        filename: target.filename,
      },
    };

    doHttpRequest("DO_DECODE", data).then((res) => {
      console.log("res");
      console.log(res.data);
      console.log(store.resultList);

      store.resultList[idx] = res.data.decode;
      store.resultList[idx].loading = false;
      console.log(store.resultList[idx]);
    });
  };
};
</script>
<style scoped src="../styles/dispbox.css"></style>
