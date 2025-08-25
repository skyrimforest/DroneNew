<template>
  <div class="all-box">
    <div class="map-box">
      <l-map
          :zoom="this.store.zoom_real"
          :center="this.store.center_real"
          :maxZoom="this.store.maxZoom"
          :minZoom="this.store.minZoom"
          @update:zoom="this.store.zoomUpdated"
          @update:center="this.store.centerUpdated"
          @update:bounds="this.store.boundsUpdated"
          :noBlockingAnimations="true"
          :useGlobalLeaflet="false"
          @click="this.store.getinfo"
          @click.right="this.store.cancelClick"
      >
        <l-control position="topright"></l-control>
        <!-- 多层次地图控制组件 -->
        <l-control-layers position="bottomright"/>
        <!-- 多层次地图 -->
        <l-tile-layer
            v-for="layer in layerList"
            :key="layer.name"
            :url="layer.layer_url"
            layer-type="base"
            :name="layer.name"
        ></l-tile-layer>
        <!-- 矩形区域 -->
        <l-rectangle
            v-for="(rectangle, index) in this.store.rectangleList"
            :key="index"
            :bounds="rectangle.bounds"
            :l-style="rectangle.style"
        ></l-rectangle>
        <!-- 圆形区域 -->
        <l-circle
            v-for="(circle, index) in this.store.circleList"
            :key="index"
            :lat-lng="circle.center"
            :radius="circle.radius"
            :color="circle.color"
        ></l-circle>
        <!-- 地图标记区域 -->
        <l-marker
            v-for="(marker, index) in this.store.markerList"
            :key="index"
            :lat-lng="marker.marker"
            :icon="getIcon(marker.iconType)"
        >
          <l-tooltip>
            <div class="tooltip-content">
              <div>经度: {{ marker.lng }}</div>
              <div>纬度: {{ marker.lat }}</div>
            </div>
          </l-tooltip>
        </l-marker
        >
        <!-- 检测区域 -->
        <l-marker
            v-for="(drone, index) in droneStationList"
            :key="index"
            :lat-lng="drone.LatLng"
            :icon="getIcon(drone.type)"
        >
          <l-tooltip>
            <div class="tooltip-content">
              <!-- <div>名称: {{ drone.LatLng }}</div> -->
              <div>名称: {{ drone.name }}</div>
              <div>经度: {{ drone.LatLng.lng }}</div>
              <div>纬度: {{ drone.LatLng.lat }}</div>
              <div>高度: {{ drone.height }}</div>
            </div>
          </l-tooltip>
        </l-marker
        >
      </l-map>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  LMap,
  LTileLayer,
  LCircle,
  LTooltip,
  LRectangle,
  LMarker,
  LControlLayers,
  LWmsTileLayer,
} from "@vue-leaflet/vue-leaflet";
import {ElNotification} from "element-plus";
import {useMapDataStore} from "@/stores/mapData";
import {APIS} from "@/modules/request";
import {doHttpRequest} from "@/modules/request.js";
import drone_pic from "assets/drone-filled.png"
import station_pic from "assets/radio-station.png"
import landmark_pic from "assets/landmark.png"
// drone: "../../assets/drone-filled.png",
// station: "../../assets/radio-station.png",
// landmark: "../../assets/landmark.png",
export default {
  name: "NewMapContainer",
  components: {
    LMap,
    LTileLayer,
    LCircle,
    LRectangle,
    LMarker,
    LTooltip,
    LControlLayers,
    LWmsTileLayer,
    ElNotification,
    L,
  },

  data() {
    return {
      index: 0,
      droneStationList: [
        [
          {
            name: "ddd-desktop@192.168.1.27:10001",
            height: 126,
            type: "station",
            LatLng: [
              {
                lat: 37,
                lng: 39.5994,
              },
            ],
          },
          {
            name: "uhd-desktop@192.168.1.29:10001",
            height: 126,
            type: "station",
            LatLng: [
              {
                lat: 37,
                lng: 40.4904,
              },
            ],
          },
          {
            name: "A drone",
            height: 175.90720193646848,
            type: "drone",
            LatLng: [
              {
                lng: 126.62760219157852,
                lat: 45.743092145334124,
              },
            ],
          },
        ],
      ],
      store: useMapDataStore(),
      icon: null,
      layerList: [
        {
          name: "谷歌款卫星地图",
          layer_url:
              "//www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
        },
        {
          name: "经典款地图",
          layer_url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        },

        // 缩放只到12,空间需要太多了
        {
          name: "高德离线中国卫星图",
          layer_url: APIS.WHOLE[1],
        },
        {
          name: "高德离线北京卫星图",
          layer_url: APIS.BEIJING[1],
        },
        {
          name: "高德离线上海卫星图",
          layer_url: APIS.SHANGHAI[1],
        },
        {
          name: "高德离线广州卫星图",
          layer_url: APIS.GUANGZHOU[1],
        },
        {
          name: "高德离线深圳卫星图",
          layer_url: APIS.SHENZHEN[1],
        },
        {
          name: "高德离线哈尔滨卫星图",
          layer_url: APIS.HARBIN[1],
        },
      ],
      // 定义不同的图标 URL
      iconUrls: {
        drone: drone_pic,
        station: station_pic,
        landmark: landmark_pic
      },
    };
  },

  mounted() {
    // let timer1;
    // const startListenFrequency = () => {
    //   clearInterval(timer1);
    //   timer1 = setInterval(update_marker, 4000);
    // };
    //
    // const update_marker = () => {
    //   doHttpRequest("UPDATE_MARKER", {}).then((res) => {
    //     this.droneStationList = res.data.data;
    //   });
    // };
    // startListenFrequency();
  },

  methods: {
    getIcon(iconType) {
      let iconUrl = this.getAssets(this.iconUrls[iconType]);
      return L.icon({
        iconUrl: iconUrl,
        iconSize: [40, 40],
        iconAnchor: [20, 20],
      });
    },

    getAssets(url) {
      return new URL(url, import.meta.url).href;
    },
  },
};
</script>

<style src="../../styles/mapbox.css"></style>
