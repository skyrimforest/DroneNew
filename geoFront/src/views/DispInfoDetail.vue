<template>
    <div class="info-container">
      <ElContainer>
        <ElHeader style="padding: 10px">
          <ElRow class="head-box">
            <ElCol :span="3">
              <ElIcon><Hide /></ElIcon>
            </ElCol>
  
            <ElCol :span="3">
              <ElIcon><Headset /></ElIcon>
            </ElCol>
  
            <ElCol :span="3">
              <ElIcon><Bell /></ElIcon>
            </ElCol>
  
            <ElCol :span="12">
              <ElSelect class="select-button" placeholder="语言" v-model="value">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                  :disabled="item.disabled"
                />
              </ElSelect>
            </ElCol>
            <ElCol :span="3">
              <ElIcon><User /></ElIcon>
            </ElCol>
          </ElRow>
        </ElHeader>
  
        <ElMain style="--el-main-padding: 0px">
          <ElRow>
            <ElCol :span="5"> </ElCol>
            <ElCol :span="10">
              <div class="drone-box">
                <span class="num-size"
                  >{{ num_cur }}
                  <p
                /></span>
                当前检测
              </div>
            </ElCol>
            <ElCol :span="6">
              <div class="drone-box">
                <span class="num-size"
                  >{{ num_past }}
                  <p
                /></span>
                过去30天
              </div>
            </ElCol>
          </ElRow>
  
          <ElRow>
            <ElCol :span="3"> </ElCol>
            <ElCol :span="10"></ElCol>
          </ElRow>
          <ElScrollbar height="170px">
            <ElTable
              :data="droneData"
              style="width: 100%"
              :row-class-name="tableRowClassName"
            >
              <ElTableColumn prop="frequency" label="频率" width="180" />
              <ElTableColumn prop="lookInfo" label="查看详情">
                <template #default="scope">
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleClick(scope.$index)"
                    >展示</el-button
                  >
                </template>
              </ElTableColumn>
            </ElTable>
          </ElScrollbar>
        </ElMain>
      </ElContainer>
    </div>
  </template>
  
  <script>
  import {
    ElIcon,
    ElHeader,
    ElContainer,
    ElMain,
    ElSelect,
    ElCol,
    ElRow,
    ElScrollbar,
    ElTable,
    ElTableColumn,
  } from "element-plus";
  import { SwitchFilled } from "@element-plus/icons-vue";
  export default {
    name: "DispInfoDetail",
    components: {
      ElHeader,
      ElContainer,
      ElMain,
      ElIcon,
      ElSelect,
      ElCol,
      ElRow,
      SwitchFilled,
      ElScrollbar,
      ElTable,
      ElTableColumn,
    },
    data: () => ({
      value: "",
      num_cur: 1,
      num_past: 644,
      options: [
        {
          value: "Option1",
          label: "Option1",
        },
        {
          value: "Option2",
          label: "Option2",
          disabled: true,
        },
      ],
      droneData: [
        {
          frequency: "单频2.4G",
        },
        {
          frequency: "单频5.8G",
        },
        {
          frequency: "单频1.4G",
        },
        {
          frequency: "单频2.4G和5.8G",
        },
      ],
    }),
    methods: {
      handleClick(index) {
        var text = this.droneData[index].frequency;
        console.log(text)
      },
    },
  };
  </script>
  
  <style scoped>
  .info-container {
    width: 300px;
    height: 300px;
    background-color: rgba(20, 20, 20, 0.8);
    backdrop-filter: blur(30px);
    border-radius: 10px;
  }
  .head-box {
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  }
  .select-button {
    background-color: rgba(20, 20, 20, 0.8);
    color: rgba(20, 20, 20, 0.8);
    width: 100px;
  }
  .drone-box {
    font-size: small;
    width: 60px;
    height: 60px;
  }
  .num-size {
    font-size: large;
    color: red;
  }
  </style>
  