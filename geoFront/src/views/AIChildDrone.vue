<template>
  <div>

    <ElRow>
      <ElCol :span="1">
      </ElCol>
      <ElCol :span="12">
        <ElButton @click="add_white">
          活跃列表
        </ElButton>
        <ElButton @click="export_white">
          休眠列表
        </ElButton>
        <ElButton @click="import_white">
          白名单
        </ElButton>
      </ElCol>
    </ElRow>
    <!-- 间隔 -->
    <el-row>
      <el-col :span="24">
        <el-col :span="24" :style="{ height: '20px' }"></el-col>
      </el-col>
    </el-row>
    <ElRow>
      <ElCol :span="1">
      </ElCol>
      <ElCol :span="22">
        <ElCard>
          <ElRow>
            <ElCol>
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
            </ElCol>
          </ElRow>
        </ElCard>
      </ElCol>
    </ElRow>
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