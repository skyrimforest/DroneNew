<template>
  <div >
    <bm-circle
      v-for="cir in circles"
      :key="cir.id"
      :center="cir.cirCenter"
      :radius="cir.cirRadius"
      stroke-color="blue"
      :stroke-opacity="0.5"
      :stroke-weight="2"
      @lineupdate="updateCirclePath"
      :editing="true"
    ></bm-circle>
  </div>
</template>
  
  
  
  <script setup>
defineProps(["title"]);
defineEmits(["update"]);
</script>
      
  <style scoped>
.el-header {
  height: 40px;
  padding: 10px;
}
.func-container {
  background-color: rgba(20, 20, 20, 0.8);
  backdrop-filter: blur(30px);
  border-radius: 10px;
  width: 900px;
  height: 300px;
}
.placeholder-box {
  width: 300px;
  height: 150px;
}
</style>