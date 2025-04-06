<template>
  <div class="meeting-panel">
    <RouterView />
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped lang="scss">
.meeting-panel {
  background: #253047;
  overflow: hidden;
  flex: 1;

  position: relative;
  .home-redirect{
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
  }
}
</style>