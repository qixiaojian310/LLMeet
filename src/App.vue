<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import Header from '@/coreComponents/Header.vue';
import {noHeaderPages} from "@/router"
const route = useRoute();

</script>

<template>
  <main class="container">
    <div class="main-layout">
      <div v-if="!noHeaderPages.some((page)=>{
        return page === route.name
      })" class="header-view">
        <Header />
      </div>
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
    background: #0d1321;
  }
}
</style>
<style>
:root {
  font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 24px;
  font-weight: 400;

  color: #0f0f0f;
  background-color: #f6f6f6;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}
</style>