<template>
  <div class="info-container">
    <ElContainer>
      <ElHeader style="width: 400px">
        <ElRow class="head-box">
          <ElCol :span="1"></ElCol>
          <ElCol :span="4">
            <ElIcon @click="closeMain"
              ><View :style="{ color: fwColor }"
            /></ElIcon>
          </ElCol>

          <ElCol :span="4">
            <ElIcon @click="closeBGM">
              <Headset :style="{ color: headsetColor }"
            /></ElIcon>
          </ElCol>

          <ElCol :span="4">
            <ElIcon @click="closeINFO"
              ><Bell :style="{ color: bellColor }"
            /></ElIcon>
          </ElCol>

          <ElCol :span="4">
            <ElIcon @click="showUser" :style="{ color: colorOK }"
              ><User
            /></ElIcon>
          </ElCol>
          <ElCol :span="6">
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
        </ElRow>
      </ElHeader>

      <ElMain v-if="mainShow">
        <ElRow>
          <ElCol :span="1"></ElCol>
          <ElCol :span="22">
            <el-descriptions
              column="3"
              border
              direction="vertical"
              align="center"
            >
              <el-descriptions-item label="后台地图" align="center">
                <el-icon><CircleCheck :style="{ color: mapOnline }" /></el-icon>
              </el-descriptions-item>
              <el-descriptions-item label="干扰模组" align="center">
                <el-icon
                  ><CircleCheck :style="{ color: disturbOnline }"
                /></el-icon>
              </el-descriptions-item>
              <el-descriptions-item label="主节点" align="center">
                <el-icon
                  ><CircleCheck :style="{ color: masterOnline }"
                /></el-icon>
              </el-descriptions-item>

              <el-descriptions-item align="center">
                <el-table
                  :data="nodeStatus"
                  stripe
                  size="small"
                  fit="true"
                  :row-class-name="tableRowClassName"
                >
                  <el-table-column
                    align="center"
                    header-align="center"
                    prop="name"
                    label="从节点名称"
                    width="200px"
                  />
                  <el-table-column
                    align="center"
                    header-align="center"
                    prop="lastupdate"
                    label="上次更新时间"
                  />
                </el-table>
              </el-descriptions-item>
            </el-descriptions>

            <el-descriptions
              column="2"
              border
              direction="vertical"
              align="center"
            >
              <el-descriptions-item label="本次检测" size="2" align="center"
                ><span :style="{ color: colorOK }">
                  <dv-digital-flop :config="current_config" />
                  <!-- {{ num_cur }} -->
                </span></el-descriptions-item
              >
              <el-descriptions-item label="30日检测" align="center">
                <span :style="{ color: colorOK }">
                  <dv-digital-flop :config="past_config" />
                  <!-- {{ num_past }} -->
                </span></el-descriptions-item
              >
            </el-descriptions>
          </ElCol>
        </ElRow>

        <ElScrollbar style="height: 200px; border-radius: 5%">
          <ElTable
            :data="mapStore.droneData"
            style="width: 100%"
            :row-class-name="tableRowClassName"
          >
            <ElTableColumn type="index" width="50" />
            <ElTableColumn prop="dronetype" label="型号" />
            <ElTableColumn prop="frequency" label="频段" />
            <ElTableColumn prop="image" label="样式">
              <template #default="scope">
                <el-image :src="getPic(mapStore.droneData[scope.$index])">
                  <template #error>
                    <div class="image-slot">
                      <el-icon><icon-picture /></el-icon>
                    </div>
                  </template>
                </el-image>
              </template>
            </ElTableColumn>
            <ElTableColumn prop="lookInfo" label="查看详情">
              <template #default="scope">
                <el-tooltip
                  class="box-item"
                  effect="dark"
                  :content="showInfo(mapStore.droneData[scope.$index])"
                  placement="top-start"
                >
                  <el-button
                    link
                    type="primary"
                    size="small"
                    @click="handleClick(scope.$index)"
                    >更多信息</el-button
                  ></el-tooltip
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
  ElNotification,
} from "element-plus";
import { SwitchFilled } from "@element-plus/icons-vue";
import { useMapDataStore } from "@/stores/mapData";
import { useMusicData } from "../stores/music";
import { doHttpRequest } from "@/modules/request.js";
import { reactive } from 'vue' // 关键导入语句
export default {
  name: "DispInfoBox",
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
    ElNotification,
  },
  setup() {
    const current_config = reactive({
      number: [0],
      content: "{nt}个",
    });
    const past_config = reactive({
      number: [0],
      content: "{nt}个",
    });
    return {
      current_config,
      past_config,
    };
  },
  computed: {
    fwColor() {
      return this.fwOK ? this.colorOK : this.colorNO;
    },
    headsetColor() {
      return this.bgmOK ? this.colorOK : this.colorNO;
    },
    bellColor() {
      return this.bellOK ? this.colorOK : this.colorNO;
    },
    mapOnline() {
      return this.mapOK ? this.colorOnline : this.colorNO;
    },
    masterOnline() {
      return this.masterOK ? this.colorOnline : this.colorNO;
    },
    childOnline() {
      return this.childOK ? this.colorChild : this.colorChild;
    },
    disturbOnline() {
      return this.disturbOK ? this.colorOnline : this.colorNO;
    },
  },
  mounted() {
    let droneTimer, nodeLifeTimer, mapLifeTimer, disturbLifeTimer;
    // 获取无人机信息 5秒运行一次
    clearInterval(droneTimer);
    droneTimer = setInterval(this.get_drone_data, 5000);
    // 获取各个节点在线情况 5秒运行一次
    clearInterval(nodeLifeTimer);
    nodeLifeTimer = setInterval(this.get_node_status, 5000);
    // 获取地图在线情况 5秒运行一次
    clearInterval(mapLifeTimer);
    mapLifeTimer = setInterval(this.get_map_status, 5000);
    // 查看干扰模组在线情况 5秒运行一次
    clearInterval(disturbLifeTimer);
    disturbLifeTimer = setInterval(this.get_disturb_status, 5000);
  },
  data: () => ({
    // Websocket
    droneWS: null,
    value: "",
    mapStore: useMapDataStore(),
    musicStore: useMusicData(),
    colorOK: "#55ff55",
    colorNO: "#ff5555",
    colorOnline: "#55ff55",
    colorChild: "#aaaa55",
    fwOK: true,
    bgmOK: false,
    bellOK: true,
    mainShow: true,
    mapOK: false,
    masterOK: false,
    childOK: false,
    disturbOK: false,
    // 子节点状态(该状态通过主站更新)
    nodeStatus: [],
    // 模块状态(地图、干扰、主站) 通过与模块之间通信更新
    moduleUpdateTime: [0, 0, 0],
    options: [
      {
        value: "中文",
        label: "中文",
      },
      {
        value: "English",
        label: "English",
        disabled: true,
      },
    ],
  }),
  methods: {
    get_drone_data() {
      // 查询后台无人机数据库,会获得当前时间5秒内所有的无人机信息
      doHttpRequest("NODE_HEARTBEAT", {})
        .then((res) => {
          if (res.data.success == true) {
            if (this.moduleUpdateTime[2] === 0) {
              this.moduleUpdateTime[2] = new Date(res.data.timestamp);
              this.masterOK = true;
              this.nodeStatus = res.data.childlist;
            } else {
              let curr_time = new Date(res.data.timestamp);
              if (
                curr_time.getTime() - this.moduleUpdateTime[2].getTime() <=
                10000
              ) {
                this.moduleUpdateTime[2] = curr_time;
                this.masterOK = true;
                this.nodeStatus = res.data.childlist;
              } else {
                this.moduleUpdateTime[2] = 0;
                this.masterOK = false;
                this.nodeStatus = [];
              }
            }
          } else {
            this.moduleUpdateTime[2] = 0;
            this.masterOK = false;
            this.nodeStatus = [];
          }
        })
        .catch((err) => {
          console.log(err);
          this.masterOK = false;
        });
    },

    get_node_status() {
      doHttpRequest("NODE_HEARTBEAT", {})
        .then((res) => {
          if (res.data.success == true) {
            if (this.moduleUpdateTime[2] === 0) {
              this.moduleUpdateTime[2] = new Date(res.data.timestamp);
              this.masterOK = true;
              this.nodeStatus = res.data.childlist;
            } else {
              let curr_time = new Date(res.data.timestamp);
              if (
                curr_time.getTime() - this.moduleUpdateTime[2].getTime() <=
                10000
              ) {
                this.moduleUpdateTime[2] = curr_time;
                this.masterOK = true;
                this.nodeStatus = res.data.childlist;
              } else {
                this.moduleUpdateTime[2] = 0;
                this.masterOK = false;
                this.nodeStatus = [];
              }
            }
          } else {
            this.moduleUpdateTime[2] = 0;
            this.masterOK = false;
            this.nodeStatus = [];
          }
        })
        .catch((err) => {
          console.log(err);
          this.masterOK = false;
        });
    },
    get_map_status() {
      doHttpRequest("DIS_HEARTBEAT", {})
        .then((res) => {
          if (res.data.success == true) {
            if (this.moduleUpdateTime[0] === 0) {
              this.moduleUpdateTime[0] = new Date(res.data.timestamp);
              this.mapOK = true;
            } else {
              let curr_time = new Date(res.data.timestamp);
              if (
                curr_time.getTime() - this.moduleUpdateTime[0].getTime() <=
                10000
              ) {
                this.moduleUpdateTime[0] = curr_time;
                this.mapOK = true;
              } else {
                this.mapOK = false;
              }
            }
          } else {
            this.mapOK = false;
          }
        })
        .catch((err) => {
          console.log(err);
          this.mapOK = false;
        });
    },
    get_disturb_status() {
      doHttpRequest("DIS_HEARTBEAT", {})
        .then((res) => {
          if (res.data.success == true) {
            if (this.moduleUpdateTime[1] === 0) {
              this.moduleUpdateTime[1] = new Date(res.data.timestamp);
              this.disturbOK = true;
            } else {
              let curr_time = new Date(res.data.timestamp);
              if (
                curr_time.getTime() - this.moduleUpdateTime[1].getTime() <=
                10000
              ) {
                this.moduleUpdateTime[1] = curr_time;
                this.disturbOK = true;
              } else {
                this.disturbOK = false;
              }
            }
          } else {
            this.disturbOK = false;
          }
        })
        .catch((err) => {
          console.log(err);
          this.disturbOK = false;
        });
    },
    closeMain() {
      this.fwOK = !this.fwOK;
      this.mainShow = !this.mainShow;
    },
    closeBGM() {
      this.bgmOK = !this.bgmOK;
      this.musicStore.bgmOn = this.bgmOK;
      if (this.bgmOK) {
        this.musicStore.playMusic("BGM");
      } else {
        this.musicStore.stopMusic("BGM");
      }
    },
    closeINFO() {
      this.bellOK = !this.bellOK;
      this.musicStore.infoOn = this.bellOK;
    },
    showUser() {
      this.musicStore.playMusic("INFO");
    },
    showInfo(infomation) {
      // 展示具体信息
      const moreInfo =
        "出现在" +
        infomation.detail.place +
        "这一位置," +
        "上次更新时间在" +
        infomation.detail.updateTime;
      return moreInfo;
    },
  },
};
</script>

<style scoped>
.el-main {
  padding: 0px;
  width: 400px;
}
.el-header {
  padding: 10px;
  height: 50px;
}
.info-container {
  background-color: rgba(20, 20, 20, 0.8);
  backdrop-filter: blur(30px);
  border-radius: 5px;
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
.el-table .warning-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>
