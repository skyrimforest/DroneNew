<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <dv-decoration7>
          <div color-white font-300>
            <Button color="#615ea8" font-color="#615ea8" border="Border6">
              无人机实时频谱报告
            </Button
            >
          </div>
        </dv-decoration7>
      </ElHeader>

      <ElMain style="--el-main-padding: 0px">
        <ElScrollbar>
          <!-- 子节点波形图部分 -->
          <ElRow>
            <ElCol :span="1"></ElCol>
            <ElCol :span="22">
              <ElCard>
                <ElRow>
                  <ElCol :span="24">
                    <div style="text-align:center;">
                      <img v-if="imgSrcTest" :src="imgSrcTest" class="spectrogram"/>
                      <div v-else>等待数据...</div>
                    </div>
                  </ElCol>
                </ElRow>
              </ElCard>
            </ElCol>
          </ElRow>

          <!-- 间隔 -->
          <el-row>
            <el-col :span="24">
              <el-col :span="24" :style="{ height: '20px' }"></el-col>
            </el-col>
          </el-row>
          <!-- 子节点波形图部分 -->
          <ElRow>
            <ElCol :span="1"></ElCol>
            <ElCol :span="22">
              <ElCard>
                <ElRow>
                  <ElCol :span="24">
                    <div style="text-align:center;">
                      <img v-if="imgSrc24" :src="imgSrc24" class="spectrogram"/>
                      <div v-else>等待数据...</div>
                    </div>
                  </ElCol>
                </ElRow>
              </ElCard>
            </ElCol>
          </ElRow>

          <!-- 间隔 -->
          <el-row>
            <el-col :span="24">
              <el-col :span="24" :style="{ height: '20px' }"></el-col>
            </el-col>
          </el-row>


          <!-- 子节点波形图部分 -->
          <ElRow>
            <ElCol :span="1"></ElCol>
            <ElCol :span="22">
              <ElCard>
                <ElRow>
                  <ElCol :span="24">
                    <div style="text-align:center;">
                      <img v-if="imgSrc58" :src="imgSrc58" class="spectrogram"/>
                      <div v-else>等待数据...</div>
                    </div>
                  </ElCol>
                </ElRow>
              </ElCard>
            </ElCol>
          </ElRow>

          <!-- 间隔 -->
          <el-row>
            <el-col :span="24">
              <el-col :span="24" :style="{ height: '20px' }"></el-col>
            </el-col>
          </el-row>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script setup>
import {ref, provide, onMounted, onUnmounted} from "vue";
import {createSSE} from "@/modules/request";
import {Button} from "@kjgl77/datav-vue3";
import {ElScrollbar} from "element-plus";


const imgSrc24 = ref(null);
const imgSrc58 = ref(null);
const imgSrcTest = ref(null);
let sse24 = null;
let sse58 = null;
let sse_test = null;

onMounted(() => {
  sse24 = createSSE("SSE_START_24", (data) => {
    imgSrc24.value = data.img; // 后端推送过来的 base64 图片
  });
  sse58 = createSSE("SSE_START_58", (data) => {
    imgSrc58.value = data.img; // 后端推送过来的 base64 图片
  });
  sse_test = createSSE("SSE_START_TEST", (data) => {
    imgSrcTest.value = data.img; // 后端推送过来的 base64 图片
  });
});

onUnmounted(() => {
  if (sse24) sse24.close();
  if (sse58) sse58.close();
  if (sse_test) sse_test.close();
});
</script>

<style>
.spectrogram {
  max-width: 100%;
  height: auto;
  border: 2px solid #ccc;
  border-radius: 8px;
}
</style>
