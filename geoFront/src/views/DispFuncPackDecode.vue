<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <dv-decoration7>
          <div color-white font-300>
            <Button color="#615ea8" font-color="#615ea8" border="Border6">
              报文解密</Button
            >
          </div>
        </dv-decoration7></ElHeader
      >
      <ElMain style="--el-main-padding: 0px; height: 100%">
        <ElScrollbar>
          <ElTable
            :data="droneData"
            style="width: 100%"
            :row-class-name="tableRowClassName"
          >
            <ElTableColumn prop="test1" label="列1" width="180" />
            <ElTableColumn prop="test2" label="列2" width="180" />
            <ElTableColumn prop="lookInfo" label="查看详情">
              <template #default="scope">
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="handleClick(scope.$index)"
                  >展示1</el-button
                >
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="handleClick(scope.$index)"
                  >展示2</el-button
                >
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
import { Button } from "@kjgl77/datav-vue3";

const droneData = [
  {
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
];
function add_white() {
  console.log("添加");
}
function export_white() {
  console.log("导出");
}
function import_white() {
  console.log("引入");
}
</script>

<style scoped src="../styles/dispbox.css"></style>
