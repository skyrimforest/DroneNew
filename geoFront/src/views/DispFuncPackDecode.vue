<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <ElRow>
          <ElCol :span="4">
            无人机报文解密
          </ElCol>
          <ElCol :span="10">
          </ElCol>
          <ElCol :span="10">
            <ElButton @click="add_white">
              添加白名单
            </ElButton>
            <ElButton @click="export_white">
              导出白名单
            </ElButton>
            <ElButton @click="import_white">
              引入白名单
            </ElButton>
          </ElCol>
        </ElRow>
      </ElHeader>
      <ElMain style="--el-main-padding: 0px;height: 100%">
        <ElScrollbar>
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
function add_white(){
  console.log("添加")
}
function export_white(){
  console.log("导出")
}
function import_white(){
  console.log("引入")
}
</script>

<style scoped src="../styles/dispbox.css"></style>