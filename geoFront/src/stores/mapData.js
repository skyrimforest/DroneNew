import { defineStore } from "pinia";
import { ElNotification } from "element-plus";

export const useMapDataStore = defineStore("mapData", {
  state: () => {
    return {
      droneData: [

      ],

      circleList: [],
      rectangleList: [],
      markerList: [],
      State: {
        // 状态:没在画
        not_drawing: "not_drawing",
        // 画圆的一号状态:该状态下获取圆心
        circle_point_state1: "circle_point_state1",
        // 画圆的二号状态:该状态下获取半径
        circle_point_state2: "circle_point_state2",
        // 画矩形的一号状态:该状态获取左上角
        rectangle_point_state1: "rectangle_point_state1",
        // 画矩形的二号状态:该状态获取右下角
        rectangle_point_state2: "rectangle_point_state2",
        // 画标记的状态:该状态获取标记坐标
        marker_point_state: "marker_point_state",
      },
      // 全局绘图状态
      drawState: "not_drawing",
      // 画圆用变量
      circle_center: null,
      circle_edge: null,
      // 画矩形用变量
      rectangle_leftup: null,
      rectangle_rightdown: null,
      // 做标记用变量
      marker_point: null,
      center_real: [44.58416560452682, 126.55151367187501],
      zoom_real: 5,
      max_zoom: 16,
      min_zoom: 5,
      bounds_real: null,
      origin_center: [44.58416560452682, 126.55151367187501],
      origin_zoom: 5,
    };
  },
  getters: {
    // 相当于vue里面的计算属性，可以缓存数据
  },
  actions: {
    // 修改缩进-放大
    zoomIn() {
      if (this.zoom_real < this.max_zoom) {
        this.zoom_real += 1;
      } else {
        this.zoom_real = this.max_zoom;
      }
    },
    // 修改缩进-缩小
    zoomOut() {
      if (this.zoom_real > this.min_zoom) {
        this.zoom_real -= 1;
      } else {
        this.zoom_real = this.min_zoom;
      }
    },
    // 绘制矩形框
    drawRect() {
      console.log(233);
      ElNotification({
        title: "开始绘图，请点击地图确定矩形左上角！",
        message: "点击取消按钮以放弃本次绘制",
        duration: 5000,
      });
      this.drawState = this.State.rectangle_point_state1;
    },
    // 绘制圆形框
    drawCir() {
      console.log(233);
      ElNotification({
        title: "开始绘图，请点击地图确定圆心！",
        message: "点击取消按钮以放弃本次绘制",
        duration: 5000,
      });
      this.drawState = this.State.circle_point_state1;
    },
    // 删除候选框
    drawRemove() {
      this.circleList.length = 0;
      this.rectangleList.length = 0;
    },

    // ----------控制区控制区域代码----------
    drawMarker() {
      ElNotification({
        title: "开始绘图，请点击地图确定控制器位置！",
        message: "点击取消按钮以放弃本次绘制",
        duration: 5000,
      });
      this.drawState = this.State.marker_point_state;
    },
    centerReturn() {
      console.log("return to center now");
      this.center_real = this.origin_center;
      this.zoom_real = this.origin_zoom;
    },
    getinfo(event) {
      console.log(event);
      switch (this.drawState) {
        case this.State.circle_point_state1:
          this.circle_center = event.latlng;
          console.log(this.circle_center);
          ElNotification({
            title: "已确定圆心，下面请点击地图确定半径长度！",
            message: "点击取消按钮以放弃本次绘制",
            duration: 5000,
          });
          this.drawState = this.State.circle_point_state2;
          break;

        case this.State.circle_point_state2:
          this.circle_edge = event.latlng;
          const distance = this.circle_edge.distanceTo(this.circle_center);
          const newCircle = {
            center: this.circle_center,
            radius: distance,
            color: "green",
          };
          this.circleList.push(newCircle);
          ElNotification({
            title: "已确定圆形！",
            message:
              "中心:" + newCircle.center + "; 半径:" + newCircle.distance,
            duration: 5000,
          });
          this.drawState = this.State.not_drawing;
          break;

        case this.State.rectangle_point_state1:
          this.rectangle_leftup = event.latlng;
          ElNotification({
            title: "已确定左上角，下面请点击地图确定右下角！",
            message: "点击取消按钮以放弃本次绘制",
            duration: 5000,
          });
          this.drawState = this.State.rectangle_point_state2;
          break;

        case this.State.rectangle_point_state2:
          this.rectangle_rightdown = event.latlng;
          const newRectangle = {
            bounds: [this.rectangle_leftup, this.rectangle_rightdown],
            style: {
              color: "green",
              weight: 3,
            },
          };
          this.rectangleList.push(newRectangle);
          ElNotification({
            title: "已确定矩形！",
            message:
              "左上角:" +
              newRectangle.bounds[0] +
              "; 右下角:" +
              newRectangle.bounds[1],
            duration: 5000,
          });
          this.drawState = this.State.not_drawing;
          break;

        case this.State.marker_point_state:
          this.marker_point = event.latlng;
          const newMarker = this.marker_point;
          this.markerList.push(newMarker);
          ElNotification({
            title: "已确定标记！",
            message: "标记坐标:" + newMarker,
            duration: 5000,
          });
          this.drawState = this.State.not_drawing;
          break;
      }
    },
    cancelClick() {
      if (this.drawState != this.State.not_drawing) {
        ElNotification({
          title: "绘图已取消！",
          message: "状态缓存已清空",
          duration: 5000,
        });
        this.drawState = this.State.not_drawing;
      } else {
        //do nothing
      }
    },
    // 更新缩放时触发
    zoomUpdated(zoom) {
      // console.log("zoom updated!")
      this.zoom_real = zoom;
      // console.log(this.zoom_real);
    },
    // 更新中心点时触发
    centerUpdated(center) {
      // console.log("center updated!")
      this.center_real = center;
      // console.log(this.center_real)
    },
    // 更新边界时触发
    boundsUpdated(bounds) {
      this.bounds_real = bounds;
    },
  },
});
