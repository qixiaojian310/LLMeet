<template>
  <div class="main-layout">
    <div class="header-view">
      <Header/>
    </div>
    <div class="content-view">
      <div class="toolbar">
        <Toolbar :buttons="navigationItems"/>
      </div>
      <div class="main-panel">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Toolbar from '@/coreComponents/Toolbar.vue';
import Header from '@/coreComponents/Header.vue';
import { fas } from '@fortawesome/free-solid-svg-icons';
import path from 'path';
import { ref } from 'vue';
import { RouterView } from 'vue-router';

const navigationItems = ref([
  {
    title: 'Home',
    icon: fas.faHouse,
    path: '/',
  },
  {
    title: 'Personal Room',
    icon: fas.faSquarePlus,
    path: '/PersonalRoom',
  },
  {
    title: 'Record convert',
    icon: fas.faFileVideo,
    path: '/RecordConvert',
  },
]);
</script>

<style scoped lang="scss">
.main-layout{
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  .header-view{
    width: 100%;
    height: 50px;
    background: #0d1321;
  }
  .content-view{
    overflow: hidden;
    flex: 1;
    display: flex;
    .toolbar{
      width: 200px;
      background: #141d34;
    }
   .main-panel{
      flex: 1;
      background: #253047;
    }
  }
}
</style>