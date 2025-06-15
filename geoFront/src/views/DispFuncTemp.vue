<template>
    <div class="func-container">
      
      <ElContainer>
        <ElMain>
          <ElRow>
            <ElCol :span="8">
              <ElCard>
                <template #header>
                  <div class="card-header">
                    <span>频谱</span>
                    <!-- <el-button class="button" text>Operation button</el-button> -->
                  </div>
                </template>
                <div class="placeholder-box"></div>
              </ElCard>
            </ElCol>
            <ElCol :span="8">
              <ElCard>
                <template #header>
                  <div class="card-header">
                    <span>时间趋势</span>
                    <!-- <el-button class="button" text>Operation button</el-button> -->
                  </div>
                </template>
                <div class="placeholder-box"></div>
              </ElCard>
            </ElCol>
            <ElCol :span="8">
              <ElCard>
                <template #header>
                  <div class="card-header">
                    <span>常见问题</span>
                    <!-- <el-button class="button" text>Operation button</el-button> -->
                  </div>
                </template>
                <div class="placeholder-box"></div>
              </ElCard>
            </ElCol>
          </ElRow>
        </ElMain>
      </ElContainer>
    </div>
  </template>
  
  <script>
  import { ElCard, ElRow, ElCol, ElContainer, ElMain } from "element-plus";
  
  export default {
    name: "DispFuncTemp",
    components: {
      ElCard,
      ElRow,
      ElCol,
      ElContainer,
      ElMain,
    },
  };
  </script>
  
  <style scoped src="../styles/dispbox.css"></style>