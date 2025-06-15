<template>
    <div class="func-container">
      <ElContainer>
        <ElHeader>
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="1">未知Wifi无人机名单</el-menu-item>
            <el-menu-item index="2">信号学习</el-menu-item>
            <el-menu-item index="3">通用检测器</el-menu-item>
            <el-menu-item index="4">未知信号</el-menu-item>
          </el-menu>
        </ElHeader>
        <ElMain style="--el-main-padding: 0px">
          <ElScrollbar height="170px">
            <ElTable :data="droneData" style="width: 100%" :row-class-name="tableRowClassName">
              <ElTableColumn prop="test1" label="列1" width="180" />
              <ElTableColumn prop="test2" label="列2" width="180" />
              <ElTableColumn prop="lookInfo" label="查看详情">
                <template #default="scope">
                  <el-button link type="primary" size="small" @click="handleClick(scope.$index)">展示1</el-button>
                  <el-button link type="primary" size="small" @click="handleClick(scope.$index)">展示2</el-button>
                </template>
              </ElTableColumn>
              <ElTableColumn prop="test3" label="列3" width="180" />
            </ElTable>
          </ElScrollbar>
        </ElMain>
      </ElContainer>
    </div>
  </template>
  
  
  
  <script setup>
  import { ref } from "vue";
  const droneData = [
    {
      test1: "test1",
      test2: "test2",
      test3: "test3",
      lookInfo: "Tom",
    },
  ];
  </script>
  <style scoped src="../styles/dispbox.css"></style>