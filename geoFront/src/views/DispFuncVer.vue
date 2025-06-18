<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <dv-decoration7>
          <div color-white font-300>
            <Button
              color="#615ea8"
              font-color="#615ea8"
              @click="getNodeInfo"
              border="Border6"
            >
              版本管理</Button
            >
          </div>
        </dv-decoration7>
      </ElHeader>
      <ElMain style="--el-main-padding: 0px">
        <ElScrollbar>
          <ElRow>
            <ElCol :span="1"> </ElCol>
            <ElCol :span="22">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <ElRow>
                      <ElCol :span="16">
                        <span style="font-size: larger">版本 0.1.0</span>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow>
                  <ElCol :span="6"> 版本特性介绍</ElCol>
                </ElRow>
                <ElRow> <ElCol :span="6"> 网站基本可用</ElCol></ElRow>
              </el-card>
            </ElCol>
          </ElRow>

          <!-- 间隔 -->
          <el-row>
            <el-col :span="24">
              <el-col :span="24" :style="{ height: '20px' }"></el-col>
            </el-col>
          </el-row>

          <ElRow>
            <ElCol :span="1"> </ElCol>
            <ElCol :span="22">
              <el-card class="box-card">
                <template #header>
                  <div class="card-header">
                    <ElRow>
                      <ElCol :span="20">
                        <span style="font-size: larger">版本 0.2.0</span>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow>
                  <ElCol :span="6"> 版本特性介绍</ElCol>
                </ElRow>
                <ElRow> <ElCol :span="6"> 现使用websocket通信</ElCol></ElRow>
              </el-card>
            </ElCol>
          </ElRow>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script setup>
import { ElScrollbar } from "element-plus";
import { ref } from "vue";
import { Button } from "@kjgl77/datav-vue3";

import { useRouter } from "vue-router";
const router = useRouter();
</script>

<style scoped src="../styles/dispbox.css"></style>
