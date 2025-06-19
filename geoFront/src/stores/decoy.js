// stores/decoy.ts
import { defineStore } from "pinia"

export const useDecoyData = defineStore("decoy", {
  state: () => ({
    scriptList: {}, // { timestamp: scriptObj }
    command: {
      patterns: {}   // { id1: { pattern: {...} }, ... }
    }
  }),
  actions: {
    async getDecoyCommand() {
      // 示例：从后端请求诱骗指令数据
      const res = await fetch("/api/decoy/command").then(r => r.json())
      this.scriptList = res.scripts || {}
      this.command.patterns = res.patterns || {}
    }
  }
})
