<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <ElRow>
          <ElCol :span="4"> 无人机事件列表 </ElCol>
          <ElCol :span="2">
            <el-switch
              v-model="judge"
              active-text="机型"
              inactive-text="时间"
              size="small"
              inline-prompt
              style="
                --el-switch-on-color: #13ce66;
                --el-switch-off-color: #0049ff;
              "
            />
          </ElCol>
          <ElCol :span="5">
            <ElSelect placeholder="节点范围" v-model="onWhichNode">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              /> </ElSelect
          ></ElCol>
          <ElCol :span="1"> </ElCol>
          <ElCol :span="12">
            <ElButton @click="add_white"> 最近7天 </ElButton>
            <ElButton @click="export_white"> 本日 </ElButton>
            <ElButton @click="import_white"> 导出事件 </ElButton>
            <ElButton @click="import_white"> 清空事件 </ElButton>
          </ElCol>
        </ElRow>
      </ElHeader>
      <ElMain style="--el-main-padding: 0px">
        <ElScrollbar>
          <ElTable
            :data="droneData"
            style="width: 100%"
            :row-class-name="tableRowClassName"
          >
            <ElTableColumn prop="test0" label="发现节点" />
            <ElTableColumn prop="test1" label="机型" />
            <!-- <ElTableColumn prop="test2" label="识别码" width="180" /> -->
            <!-- <ElTableColumn prop="test3" label="出现次数" width="180" /> -->
            <!-- <ElTableColumn prop="test4" label="发现时间" width="180" /> -->
            <!-- <ElTableColumn prop="test5" label="时长(秒)" width="180" /> -->
            <ElTableColumn prop="test6" label="工作频率" />
            <ElTableColumn prop="test7" label="发现时间" />
            <ElTableColumn prop="test8" label="发现位置" />
            <!-- <ElTableColumn prop="test9" label="传感器" width="180" /> -->
            <ElTableColumn prop="lookInfo" label="操作">
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
            <!-- <ElTableColumn prop="test3" label="列3" width="180" /> -->
          </ElTable>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script setup>
import { ElSwitch } from "element-plus";
import { ref } from "vue";
var judge = ref(true);
const droneData = [
  {
    test0: "主节点",
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
  {
    test0: "子节点1",
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
  {
    test0: "子节点2",
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
  {
    test0: "子节点3",
    test1: "test1",
    test2: "test2",
    test3: "test3",
    lookInfo: "Tom",
  },
];
const options = [
  {
    value: "全部节点",
    label: "全部节点",
  },
  {
    value: "主节点",
    label: "主节点",
  },
  {
    value: "从节点一号",
    label: "从节点一号",
    disabled: true,
  },
  {
    value: "从节点二号",
    label: "从节点二号",
    disabled: true,
  },
  {
    value: "从节点三号",
    label: "从节点三号",
    disabled: true,
  },
];
const onWhichNode = ref("全部节点");
</script>

<!-- <style scoped src="../styles/dispbox.css"></style> -->
