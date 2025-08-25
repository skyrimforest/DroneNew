<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>
        <dv-decoration7>
          <div color-white font-300>
            <Button color="#615ea8" font-color="#615ea8" border="Border6">
              无人机波形统计报告
            </Button
            >
          </div>
        </dv-decoration7>
      </ElHeader>

      <ElMain style="--el-main-padding: 0px">
        <ElScrollbar>
          <!-- 间隔 -->
          <el-row>
            <el-col :span="24">
              <el-col :span="24" :style="{ height: '20px' }"></el-col>
            </el-col>
          </el-row>

          <!-- 主节点波形图部分 -->
          <ElRow>
            <ElCol :span="1"></ElCol>
            <ElCol :span="22">
              <ElCard>
                <ElRow>
                  <ElCol :span="24">
                    <v-chart class="chart" :option="pic_options[0]"/>
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
                    <v-chart class="chart" :option="pic_options[1]"/>
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
                    <v-chart class="chart" :option="pic_options[2]"/>
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
                    <v-chart class="chart" :option="pic_options[3]"/>
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
import {ref, provide, onMounted} from "vue";

// echarts的引入
import {use} from "echarts/core";
import {CanvasRenderer} from "echarts/renderers";
import {PieChart, LineChart, BarChart} from "echarts/charts";
import {Button} from "@kjgl77/datav-vue3";

import {doHttpRequest, getWebSocket} from "@/modules/request.js";

import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent,
} from "echarts/components";

import VChart, {THEME_KEY} from "vue-echarts";
import {ElScrollbar} from "element-plus";

use([
  CanvasRenderer,
  PieChart,
  LineChart,
  BarChart,
  TitleComponent,
  ToolboxComponent,
  DataZoomComponent,
  DataZoomComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

provide(THEME_KEY, "dark");

onMounted(() => {
  startListenFrequency();
});

// ----------获取频率数据----------
const option_master = {
  backgroundColor: "#2c343c",
  title: {
    text: "Frequency Master:",
    left: "center",
    top: 20,
    textStyle: {
      color: "#ccc",
    },
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: false,
      },
      saveAsImage: {
        pixelRatio: 2,
      },
    },
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  grid: {
    bottom: 90,
  },
  dataZoom: [
    {
      type: "inside",
    },
    {
      type: "slider",
    },
  ],
  xAxis: {
    type: "category",
    data: [1, 2, 3, 4, 5, 6, 7],
    silent: false,
    splitLine: {
      show: false,
    },
    splitArea: {
      show: false,
    },
  },
  yAxis: {
    type: "value",
    splitArea: {
      show: false,
    },
  },
  series: [
    {
      data: [0, 0, 0, 0, 0, 0, 0],
      type: "bar",
    },
  ],
};

const option_child1 = {
  backgroundColor: "#2c343c",
  title: {
    text: "Frequency Child1:",
    left: "center",
    top: 20,
    textStyle: {
      color: "#ccc",
    },
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: false,
      },
      saveAsImage: {
        pixelRatio: 2,
      },
    },
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  grid: {
    bottom: 90,
  },
  dataZoom: [
    {
      type: "inside",
    },
    {
      type: "slider",
    },
  ],
  xAxis: {
    type: "category",
    data: [1, 2, 3, 4, 5, 6, 7],
    silent: false,
    splitLine: {
      show: false,
    },
    splitArea: {
      show: false,
    },
  },
  yAxis: {
    type: "value",
    splitArea: {
      show: false,
    },
  },
  series: [
    {
      data: [0, 0, 0, 0, 0, 0, 0],
      type: "bar",
    },
  ],
};

const option_child2 = {
  backgroundColor: "#2c343c",
  title: {
    text: "Frequency Child2:",
    left: "center",
    top: 20,
    textStyle: {
      color: "#ccc",
    },
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: false,
      },
      saveAsImage: {
        pixelRatio: 2,
      },
    },
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  grid: {
    bottom: 90,
  },
  dataZoom: [
    {
      type: "inside",
    },
    {
      type: "slider",
    },
  ],
  xAxis: {
    type: "category",
    data: [1, 2, 3, 4, 5, 6, 7],
    silent: false,
    splitLine: {
      show: false,
    },
    splitArea: {
      show: false,
    },
  },
  yAxis: {
    type: "value",
    splitArea: {
      show: false,
    },
  },
  series: [
    {
      data: [0, 0, 0, 0, 0, 0, 0],
      type: "bar",
    },
  ],
};

const option_child3 = {
  backgroundColor: "#2c343c",
  title: {
    text: "Frequency Child3:",
    left: "center",
    top: 20,
    textStyle: {
      color: "#ccc",
    },
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: false,
      },
      saveAsImage: {
        pixelRatio: 2,
      },
    },
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  grid: {
    bottom: 90,
  },
  dataZoom: [
    {
      type: "inside",
    },
    {
      type: "slider",
    },
  ],
  xAxis: {
    type: "category",
    data: [1, 2, 3, 4, 5, 6, 7],
    silent: false,
    splitLine: {
      show: false,
    },
    splitArea: {
      show: false,
    },
  },
  yAxis: {
    type: "value",
    splitArea: {
      show: false,
    },
  },
  series: [
    {
      data: [0, 0, 0, 0, 0, 0, 0],
      type: "bar",
    },
  ],
};

const x_y_datas = ref([]);
const pic_options = ref([
  option_master,
  option_child1,
  option_child2,
  option_child3,
]);

let timer1;
let timer2;
const update_option = () => {
  for (let i = 0; i < x_y_datas.value.length; i++) {
    pic_options.value[i].title.text = "Frequency:" + x_y_datas.value[i].name;
    pic_options.value[i].xAxis.data = x_y_datas.value[i].data.x;
    pic_options.value[i].series[0].data = x_y_datas.value[i].data.y;
  }
};
const update_data = () => {
  x_y_datas.value = [];
  doHttpRequest("FREQUENCY", {}).then((res) => {
    x_y_datas.value.push(...res.data);
  });
  doHttpRequest("FREQUENCY_CHILD", {}).then((res) => {
    x_y_datas.value.push(...res.data);
  });
};
const startListenFrequency = () => {
  clearInterval(timer1);
  timer1 = setInterval(update_data, 4000);
  clearInterval(timer2);
  timer2 = setInterval(update_option, 5000);
};
</script>

<style>
.chart {
  height: 400px;
  widows: 100%;
}
</style>
