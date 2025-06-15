<template>
  <!-- 可拖拽的 div -->
  <div ref="draggableDiv" class="draggable" @mousedown="startDrag">
    <BorderBox8 class="border-box-wrapper">
      <DispInfoBox> </DispInfoBox>
    </BorderBox8>
  </div>
</template>
<script setup>
import { BorderBox8 } from "@kjgl77/datav-vue3";

import { ref } from "vue";
import DispInfoBox from "./DispInfoBox.vue";
// 初始化可拖拽的 div 的引用
const draggableDiv = ref(null);
// 组件初始位置
let boxPos = ref({
  x: 0,
  y: 0,
});
// 鼠标初始位置
let startPos = ref({
  x: 0,
  y: 0,
});
let isMove = ref(0);
// 处理开始拖拽的函数
const startDrag = (event) => {
  const { clientX, clientY } = event;
  boxPos.value = {
    x: draggableDiv.value.offsetLeft,
    y: draggableDiv.value.offsetTop,
  };
  startPos.value = {
    x: clientX,
    y: clientY,
  };

  isMove.value = 1;
  draggableDiv.value.style.cursor = "grab";
  const moveHandler = (event) => {
    if (!isMove.value) return;
    // 计算新的位置
    const { clientX, clientY } = event;
    const newClientX = clientX;
    const newClientY = clientY;
    const x = newClientX - startPos.value.x;
    const y = newClientY - startPos.value.y;

    draggableDiv.value.style.left = `${x + boxPos.value.x}px`;
    draggableDiv.value.style.top = `${y + boxPos.value.y}px`;
  };
  const upHandler = (event) => {
    isMove.value = 0;
    document.body.style.cursor = "default";
    document.removeEventListener("mousemove", moveHandler);
    document.removeEventListener("mouseup", upHandler);
  };
  document.addEventListener("mousemove", moveHandler);
  document.addEventListener("mouseup", upHandler);
};
</script>
<style scoped>
.draggable {
  width: 430px;
  height: 560px;
}

.border-box-wrapper {
  position: relative;
  z-index: 0;
  padding: 10px;
}
</style>
