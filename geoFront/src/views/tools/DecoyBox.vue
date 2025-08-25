<template>
  <div class="decoy-box">
    <h4>诱骗策略</h4>
    <pre>{{ pattern }}</pre>
  </div>
</template>

<script setup>
defineProps({
  pattern: Object
})
</script>

<style scoped>
.decoy-box {
  padding: 1rem;
  margin: 1rem 0;
  background: #e0f7fa;
  border-left: 4px solid #039be5;
  border-radius: 6px;
}
</style>
