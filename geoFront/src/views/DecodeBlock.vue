<template>
  <div class="decode-block">
    <h3>{{ title }}</h3>
    <p>候选帧数：{{ target.total_candidates }}，成功解码：{{ target.total_decoded }}，CRC 错误：{{ target.crc_errors }}</p>

    <div
      v-for="chunk in target.frames"
      :key="chunk.chunk_index"
      class="chunk-section"
    >
      <h4>Chunk #{{ chunk.chunk_index }}（共 {{ chunk.detected_frame_count }} 帧）</h4>
      <div
        class="frame"
        v-for="frame in chunk.frames"
        :key="frame.frame_index"
        :class="{ 'ok': frame.decoded && frame.crc_ok, 'fail': !frame.decoded }"
      >
        <p>帧 #{{ frame.frame_index }} - {{ frame.decoded ? '✅ 解码成功' : '❌ 解码失败' }}</p>
        <p v-if="frame.payload"><strong>Payload:</strong> {{ frame.payload }}</p>
        <p v-if="frame.error"><strong>错误信息:</strong> {{ frame.error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  target: Object,
  title: String,
})
</script>

<style scoped>
.decode-block {
  padding: 1rem;
}
.chunk-section {
  border-top: 1px dashed #999;
  padding-top: 0.5rem;
  margin-top: 1rem;
}
.frame {
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: #f2f2f2;
  border-radius: 6px;
}
.frame.ok {
  border-left: 5px solid #67C23A;
}
.frame.fail {
  border-left: 5px solid #F56C6C;
  background: #fdf2f2;
}
</style>
