<template>
    <div class="new-login-box">
        <el-row>
            <el-col><el-input></el-input></el-col>
        </el-row>

    </div>
</template>

<script >
import { ElRow, ElCol, ElNotification, ElInput, ElSpace } from "element-plus";

export default {
    name: "NewLoginBox",
    components: {
        ElRow,
        ElCol, ElInput, ElSpace
    },
}

</script>


<style scoped>
.new-loginx-box {
    text-align: center;
    width: 450px;
    height: 200px;
    margin: 10% auto;
    background-color: rgba(255, 255, 127, 1);
    border-radius: 10px;
}
</style>