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
              获取当前在线节点信息</Button
            >
          </div>
        </dv-decoration7>
        <!-- <ElButton @click="getNodeInfo">获取当前在线节点信息</ElButton> -->
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
                        <span style="font-size: larger"> 主节点 </span>
                      </ElCol>
                      <ElCol :span="8">
                        <el-icon
                          v-if="nodeStatus[0] == 1"
                          :style="{ color: colorOnline }"
                          ><Check
                        /></el-icon>
                        <el-icon
                          v-else-if="nodeStatus[0] == 0"
                          :style="{ color: colorOffline }"
                          ><Close
                        /></el-icon>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <!-- <ElRow>
                  <ElCol :span="6"> 获取相关信息: </ElCol>
                  <ElCol :span="8">
                    <ElInput placeholder="todo"></ElInput>
                  </ElCol>
                </ElRow> -->
                <ElRow
                  ><ElCol>
                    <el-descriptions
                      column="3"
                      border
                      direction="vertical"
                      align="center"
                    >
                      <el-descriptions-item label="节点名称" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[0] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[0].node_name }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="节点IP" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[0] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[0].node_ip }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="节点端口" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[0] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[0].node_port }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="更新时间" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[0] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[0].last_updated }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="物理地址" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[0] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[0].geo_place }}
                        </span>
                      </el-descriptions-item>
                    </el-descriptions>
                  </ElCol>
                </ElRow>
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
                      <ElCol :span="16">
                        <span style="font-size: larger">从节点一号</span>
                      </ElCol>
                      <ElCol :span="8">
                        <el-icon
                          v-if="nodeStatus[1] == 1"
                          :style="{ color: colorOnline }"
                          ><Check
                        /></el-icon>
                        <el-icon
                          v-else-if="nodeStatus[1] == 0"
                          :style="{ color: colorOffline }"
                          ><Close
                        /></el-icon>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow
                  ><ElCol>
                    <el-descriptions
                      column="3"
                      border
                      direction="vertical"
                      align="center"
                    >
                      <el-descriptions-item label="节点名称" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[1] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[1].node_name }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="节点IP" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[1] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[1].node_ip }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="节点端口" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[1] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[1].node_port }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="更新时间" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[1] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[1].last_updated }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="物理地址" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[1] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[1].geo_place }}
                        </span>
                      </el-descriptions-item>
                    </el-descriptions>
                  </ElCol>
                </ElRow>
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
                      <ElCol :span="16">
                        <span style="font-size: larger">从节点二号</span>
                      </ElCol>
                      <ElCol :span="8">
                        <el-icon
                          v-if="nodeStatus[2] == 1"
                          :style="{ color: colorOnline }"
                          ><Check
                        /></el-icon>
                        <el-icon
                          v-else-if="nodeStatus[2] == 0"
                          :style="{ color: colorOffline }"
                          ><Close
                        /></el-icon>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow
                  ><ElCol>
                    <el-descriptions
                      column="3"
                      border
                      direction="vertical"
                      align="center"
                    >
                      <el-descriptions-item label="节点名称" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[2] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[2].node_name }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="节点IP" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[2] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[2].node_ip }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="节点端口" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[2] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[2].node_port }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="更新时间" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[2] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[2].last_updated }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="物理地址" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[2] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[2].geo_place }}
                        </span>
                      </el-descriptions-item>
                    </el-descriptions>
                  </ElCol>
                </ElRow>
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
                      <ElCol :span="16">
                        <span style="font-size: larger">从节点三号</span>
                      </ElCol>
                      <ElCol :span="8">
                        <el-icon
                          v-if="nodeStatus[3] == 1"
                          :style="{ color: colorOnline }"
                          ><Check
                        /></el-icon>
                        <el-icon
                          v-else-if="nodeStatus[3] == 0"
                          :style="{ color: colorOffline }"
                          ><Close
                        /></el-icon>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow
                  ><ElCol>
                    <el-descriptions
                      column="3"
                      border
                      direction="vertical"
                      align="center"
                    >
                      <el-descriptions-item label="节点名称" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[3] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[3].node_name }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="节点IP" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[3] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[3].node_ip }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="节点端口" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[3] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[3].node_port }}
                        </span>
                      </el-descriptions-item>
                      <el-descriptions-item label="更新时间" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[3] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[3].last_updated }}
                        </span>
                      </el-descriptions-item>

                      <el-descriptions-item label="物理地址" align="center">
                        <span
                          :style="{
                            color:
                              nodeStatus[3] == 1 ? colorOnline : colorOffline,
                          }"
                        >
                          {{ nodeInfo[3].geo_place }}
                        </span>
                      </el-descriptions-item>
                    </el-descriptions>
                  </ElCol>
                </ElRow>
              </el-card>
            </ElCol>
          </ElRow>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { doHttpRequest } from "@/modules/request.js";
import { Button } from "@kjgl77/datav-vue3";

const colorOnline = ref("#55ff55");
const colorOffline = ref("#ff5555");
const nodeStatus = ref([0, 0, 0, 0]);
const nodeInfo = ref([
  {
    node_name: "master",
    node_ip: "0.0.0.0",
    node_port: 0,
    last_updated: 0,
    geo_place: "计算机学院楼",
  },
  {
    node_name: "child1",
    node_ip: "0.0.0.0",
    node_port: 0,
    last_updated: 0,
    geo_place: "雅园",
  },
  {
    node_name: "child2",
    node_ip: "0.0.0.0",
    node_port: 0,
    last_updated: 0,
    geo_place: "和园",
  },
  {
    node_name: "child3",
    node_ip: "0.0.0.0",
    node_port: 0,
    last_updated: 0,
    geo_place: "勇园",
  },
]);
// todo 需要把这个里面的模块改为随node数量变化的
const getNodeInfo = () => {
  doHttpRequest("NODE_INFO").then((res) => {
    nodeInfo.value = res.data.data;
    let len = res.data.data.length;
    for (let i = 0; i < len; i++) {
      nodeStatus.value[i] = 1;
    }
  });
};

const handleOpen = (key, keyPath) => {
  console.log(key, keyPath);
};
const handleClose = (key, keyPath) => {
  console.log(key, keyPath);
};
</script>

<style scoped src="../styles/dispbox.css"></style>
