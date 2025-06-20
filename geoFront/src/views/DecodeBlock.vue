<template>
  <div class="decode-block">
    <dv-loading v-if="target.loading">
      <div color-white>解包加载中...</div>
    </dv-loading>
    <div v-if="!target.loading">
      <h3>{{ title }}</h3>
      <p>
        候选帧数：{{ target.total_candidates }}，成功解码：{{
          target.total_decoded
        }}，CRC 错误：{{ target.crc_errors }}
      </p>

      <div
        v-for="chunk in target.frames"
        :key="chunk.chunk_index"
        class="chunk-section"
      >
        <h4>
          Chunk #{{ chunk.chunk_index }}（共
          {{ chunk.detected_frame_count }} 帧）
        </h4>
        <div
          class="frame"
          v-for="frame in chunk.frames"
          :key="frame.frame_index"
          :class="{ ok: frame.decoded && frame.crc_ok, fail: !frame.decoded }"
        >
          <p>
            帧 #{{ frame.frame_index }} -
            {{ frame.decoded ? "✅ 解码成功" : "❌ 解码失败" }}
          </p>
          <p v-if="frame.payload">
            <strong>Payload:</strong> {{ frame.payload }}
          </p>
          <p v-if="frame.error"><strong>错误信息:</strong> {{ frame.error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  target: Object,
  title: String,
});
</script>

<style scoped>
.decode-block {
  padding: 1rem;
}
.chunk-section {
  border-top: 1px dashed #3f3f3f;
  padding-top: 0.5rem;
  margin-top: 1rem;
}
.frame {
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: #3f3f3f;
  border-radius: 6px;
}
.frame.ok {
  border-left: 5px solid #67c23a;
  background: #3f5f3f;
}
.frame.fail {
  border-left: 5px solid #f56c6c;
  background: #5f3f3f;
}
</style>
