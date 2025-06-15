<template>
  <div>
      <div class="menu-box">
          <div class="button-container">
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="testClick">
                      地图模式切换
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="onZoomInClick">
                      地图界面放大
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="onZoomOutClick">
                      地图界面缩小
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)">
                      返回防控区
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)">
                      矩形预警圈
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)">
                      六边形预警圈
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="onNewCircleClick">
                      圆形预警圈
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="onRmAllZoneClick">
                      擦除预警圈</ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)">
                      设置控制器坐标
                  </ElButton>
              </ElRow>
              <ElRow>
                  <ElButton class="custom-button" color="rgba(20,20,20,0.8)" @click="onShowCenterClick">
                      返回中心点
                  </ElButton>
              </ElRow>
          </div>
      </div>

      <div id="map-container" ref="mapContainer"></div>

  </div>
</template>

<script setup>
import 'mapbox-gl/dist/mapbox-gl.css';

import { useMapStore } from "../stores/map.js";
import { onMounted, ref } from "vue";

const mapStore = useMapStore()  // 地图仓库
const mapContainer = ref(null)

const initMap = async () => {
  await mapStore.initMap(mapContainer.value)
}

onMounted(() => {
  initMap()
})

</script>

<style scoped>
.map-box {
  z-index: 5;
}

.bm-view {
  width: 100%;
  height: 800px;
}

#map-container {
  height: 100vh;
  width: 100vw;
  /* margin-right: 5px; */
  /*box-shadow: 0 5px 5px 0 rgba(0, 0, 0, 0.2); !* 在底部添加阴影 *!*/
}

.menu-box {
  position: absolute;
  top: 50px;
  left: 20px;
  backdrop-filter: blur(10px);
  border-radius: 10px;
  z-index: 2;
}

.custom-button {
  width: 120px;
}
</style>
