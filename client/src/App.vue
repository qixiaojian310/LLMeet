<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <main class="container">
    <div class="main-layout">
      <RouterView />
    </div>
  </main>
</template>

<style scoped lang="scss">
.container {
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.main-layout {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;

  .header-view {
    width: 100%;
    height: 50px;
    background: var(--primary-background-color);
  }
}
</style>
<style>
:root {
  font-family: Arial, sans-serif;
  font-size: 16px;
  line-height: 24px;
  font-weight: 400;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}
</style>
