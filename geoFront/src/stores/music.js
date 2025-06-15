import { defineStore } from "pinia";
import { Howl, Howler } from "howler"

export const useMusicData = defineStore('music', {
    state: () => {
        const getAssets = (url) => {
            return new URL(url, import.meta.url).href;
        }
        const BGM = new Howl({
            src: [getAssets('../assets/BGM.mp3')],
            volume: 0.1,
            loop: true,
        })
        const INFO = new Howl({
            src: [getAssets('../assets/Info.mp3')],
            volume: 0.5,
        })
        return {
            // 方法
            bgmPlay: BGM,
            infoPlay: INFO,
            // 是否暂停
            bgmOn: false,
            infoOn: true,
        }
    },
    getters: { // 相当于vue里面的计算属性，可以缓存数据

    },
    actions: { // 可以通过actions 方法，改变 state 里面的值。
        playMusic(musicType) {
            switch (musicType) {
                case "BGM": {
                    if (this.bgmOn) {
                        this.bgmPlay.play();
                    }
                    break;
                }
                case "INFO": {
                    if (this.infoOn) {
                        this.infoPlay.play();
                    }
                    break;
                }
            }
        },
        stopMusic(musicType) {
            switch (musicType) {
                case "BGM": {
                    this.bgmPlay.pause();
                    break;
                }
            }
        },
    }
})


