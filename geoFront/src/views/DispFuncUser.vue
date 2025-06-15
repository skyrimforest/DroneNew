<template>
  <div class="func-container">
    <ElContainer>
      <ElHeader>账户设置</ElHeader>
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
                        <span style="font-size: larger">修改密码</span>
                      </ElCol>
                      <ElCol :span="4">
                        <ElButton type="warning" @click="confirm_update"
                          >确认提交</ElButton
                        >
                      </ElCol>
                      <ElCol :span="4">
                        <ElButton type="warning" @click="confirm_update"
                          >取消提交</ElButton
                        >
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElRow>
                  <ElCol :span="6"> 请输入原密码: </ElCol>
                  <ElCol :span="8">
                    <ElInput
                      v-model="username"
                      placeholder="请输入原密码"
                    ></ElInput>
                  </ElCol>
                </ElRow>
                <ElRow>
                  <br />
                </ElRow>
                <ElRow>
                  <ElCol :span="6"> 请输入新密码: </ElCol>
                  <ElCol :span="8">
                    <ElInput
                      v-model="username"
                      placeholder="请输入新密码"
                    ></ElInput>
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
                      <ElCol :span="20">
                        <span style="font-size: larger">用户管理</span>
                      </ElCol>
                      <ElCol :span="4">
                        <ElButton type="success" @click="add_user">
                          添加用户
                        </ElButton>
                      </ElCol>
                    </ElRow>
                  </div>
                </template>
                <ElTable
                  :data="droneData"
                  style="width: 100%"
                  :row-class-name="tableRowClassName"
                >
                  <ElTableColumn prop="test1" label="ID" />
                  <ElTableColumn prop="test2" label="用户名" />
                  <ElTableColumn prop="test3" label="身份" />

                  <ElTableColumn prop="lookInfo" label="访问权限">
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
                </ElTable>
              </el-card>
            </ElCol>
          </ElRow>
        </ElScrollbar>
      </ElMain>
    </ElContainer>
  </div>
</template>

<script setup>
import { ElButton } from "element-plus";
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
const router = useRouter();
var tarpwd = ref("");
var oripwd = ref("");
var username = ref("");
const logOut = () => {
  router.replace({ name: "LoginPage" });
};
function add_user() {}
</script>

<style scoped src="../styles/dispbox.css"></style>
