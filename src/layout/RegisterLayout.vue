<template>
  <div class="register-panel">
    <div class="controller-panel">
      <RouterView />
    </div>
    <div class="register-bg" :style="{background: `url(${registerBGURL}) no-repeat center center`, backgroundSize: 'auto 100%'}">
     
    </div>
  </div>
</template>

<script setup lang="ts">
const registerBGURL = new URL('@/assets/login-bg.png', import.meta.url).href
</script>

<style scoped lang="scss">
.register-panel {
  background: var(--primary-background-color);
  overflow: hidden;
  flex: 1;
  display: flex;
}
.controller-panel{
  height: 100%;
  width: 500px;
}
.register-bg{
  height: 100%;
  flex: 1;
}
</style>