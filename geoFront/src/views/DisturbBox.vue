<template>
  <div class="disbox">
    <!-- "child pattern"{{ pattern }} -->
    <el-card>
      <!-- 头部区域 -->
      <template #header>
        <div class="card-header">
          <el-row>
            <el-col :span="12">
              <el-tag>{{ patternName }}</el-tag>
            </el-col>
            <el-col :span="12">
              <el-select
                v-show="patternPower"
                v-model="power"
                placeholder="功率"
              >
                <el-option
                  v-for="item in patternPower"
                  :key="item"
                  :label="item"
                  :value="item"
                >
                </el-option>
              </el-select>
            </el-col>
          </el-row>
        </div>
      </template>

      <!-- 主体区域 -->
      <!-- 无参数 -->
      <el-table
        v-if="tableExist[0]"
        :data="scriptGroup[0]"
        stripe
        style="width: 100%"
      >
        <ElTableColumn prop="script" label="脚本"></ElTableColumn>
        <ElTableColumn prop="lookInfo" label="操作">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStart(tableIndex[0], scope.row, scope.$index)"
              >运行干扰</el-button
            >
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStop(tableIndex[0], scope.row, scope.$index)"
              >关闭</el-button
            >
          </template>
        </ElTableColumn>
      </el-table>
      <!-- 二参数 -->
      <el-table v-if="tableExist[1]" :data="scriptGroup[1]" stripe>
        <ElTableColumn prop="script" label="脚本"></ElTableColumn>
        <ElTableColumn prop="args1" :label="`${configGroup[1][0]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[0]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="args2" :label="`${configGroup[1][1]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[1]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="lookInfo" label="操作">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStart(tableIndex[1], scope.row, scope.$index)"
              >运行干扰</el-button
            >
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStop(tableIndex[1], scope.row, scope.$index)"
              >关闭</el-button
            >
          </template>
        </ElTableColumn>
      </el-table>
      <!-- 四参数 -->
      <el-table
        v-if="tableExist[2]"
        :data="scriptGroup[2]"
        stripe
        style="width: 100%"
      >
        <ElTableColumn prop="script" label="脚本"></ElTableColumn>
        <ElTableColumn prop="args1" :label="`${configGroup[2][0]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[0]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="args2" :label="`${configGroup[2][1]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[1]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="args3" :label="`${configGroup[2][2]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[2]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="args4" :label="`${configGroup[2][3]}`">
          <template v-slot="scope">
            <ElInput v-model="scope.row.args[3]"> </ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="lookInfo" label="操作">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStart(tableIndex[2], scope.row, scope.$index)"
              >运行干扰</el-button
            >
            <el-button
              link
              type="primary"
              size="small"
              @click="handleClickStop(tableIndex[2], scope.row, scope.$index)"
              >关闭</el-button
            >
          </template>
        </ElTableColumn>
      </el-table>

      <!-- 脚部区域 -->
      <!-- <template #footer>Footer content</template> -->
    </el-card>
  </div>
</template>

<script setup>
import { ref, toRefs, onMounted, onUpdated } from "vue";
import { ElInput } from "element-plus";
import { doHttpRequest } from "@/modules/request";

import { useDisturbData } from "@/stores/disturb";
const store = useDisturbData();

const props = defineProps({
  pattern: Object,
});
const { pattern } = toRefs(props);
const patternName = ref("留空");
const patternPower = ref("");
const power = ref("");
// 表的序号
const tableIndex = ref([0, 1, 2]);
// 表是否应该存在
const tableExist = ref([0, 0, 0]);
// 配置组
const configGroup = ref([[], [], []]);
// 脚本组
const scriptGroup = ref([[], [], []]);
onMounted(() => {
  patternName.value = pattern.value.name;
  patternPower.value = pattern.value.power;

  // 根据args分为不同的参数组:无args,有两个args,有四个args
  for (let i = 0; i < pattern.value.commands.length; i++) {
    const config = pattern.value.commands[i].command.config;
    const files = pattern.value.commands[i].command.files;
    switch (config.length) {
      case 0:
      case 1: {
        tableExist.value[0] = 1;
        configGroup.value[0] = config;
        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[0].push({
            script: files[j],
          });
        }
        break;
      }
      case 2:
        tableExist.value[1] = 1;
        configGroup.value[1] = config;

        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[1].push({
            script: files[j],
            args: ["", ""],
          });
        }
        break;
      case 4:
        tableExist.value[2] = 1;
        configGroup.value[2] = config;

        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[2].push({
            script: files[j],
            args: ["", "", "", ""],
          });
        }
        break;
    }
  }
});
onUpdated(() => {
  patternName.value = pattern.value.name;
  patternPower.value = pattern.value.power;

  const power = ref("");
  // 表的序号
  const tableIndex = ref([0, 1, 2]);
  // 表是否应该存在
  const tableExist = ref([0, 0, 0]);
  // 配置组
  const configGroup = ref([[], [], []]);
  // 脚本组
  const scriptGroup = ref([[], [], []]);

  // 根据args分为不同的参数组:无args,有两个args,有四个args
  for (let i = 0; i < pattern.value.commands.length; i++) {
    const config = pattern.value.commands[i].command.config;
    const files = pattern.value.commands[i].command.files;
    switch (config.length) {
      case 0:
      case 1: {
        tableExist.value[0] = 1;
        configGroup.value[0] = config;
        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[0].push({
            script: files[j],
          });
        }
        break;
      }
      case 2:
        tableExist.value[1] = 1;
        configGroup.value[1] = config;

        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[1].push({
            script: files[j],
            args: ["", ""],
          });
        }
        break;
      case 4:
        tableExist.value[2] = 1;
        configGroup.value[2] = config;

        for (let j = 0; j < files.length; j++) {
          scriptGroup.value[2].push({
            script: files[j],
            args: ["", "", "", ""],
          });
        }
        break;
    }
  }
});
// 组合出脚本运行的指令
const get_script = (argIndex, realPattern, realRow, realIndex) => {
  // argIndex表明用的是哪个参数组
  const argList = [];
  const configList = configGroup.value[argIndex];
  for (let i = 0; i < configList.length; i++) {
    if (configList[i] === null) continue;
    argList.push({
      [configList[i]]: realRow.args[i],
    });
  }
  const startScript = {
    command: realRow.script,
    arguments: argList,
    pattern: realPattern.dirname,
    power: power.value + "",
  };
  return startScript;
};
// 开启脚本运行
const handleClickStart = (aindex, row, index) => {
  const script = get_script(aindex, pattern.value, row, index);
  doHttpRequest("RUN_SCRIPT", script)
    .then((res) => {
      store.scriptList[res.data.data.timestamp] = res.data.data;
      console.log(store.scriptList);
    })
    .catch((err) => {
      console.log(err);
    });
};
// 关闭脚本运行
const handleClickStop = (aindex, row, index) => {
  const script = get_script(aindex, pattern.value, row, index);
  doHttpRequest("STOP_SCRIPT", script)
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped src="../styles/disturbbox.css"></style>
