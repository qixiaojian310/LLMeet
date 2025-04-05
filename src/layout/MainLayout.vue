<template>
  <div class="content-view">
    <div class="toolbar">
      <Toolbar :buttons="navigationItems" />
    </div>
    <div class="main-panel-box">
      <div class="title">{{ router.currentRoute.value.name }}</div>
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Toolbar from '@/coreComponents/Toolbar.vue';
import Header from '@/coreComponents/Header.vue';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import { router } from '@/router';

const navigationItems = ref([
  {
    title: 'Home',
    icon: fas.faHouse,
    path: '',
  },
  {
    title: 'Join Conference',
    icon: fas.faSquarePlus,
    path: 'meeting-join-form',
  },
  {
    title: 'Records',
    icon: fas.faFileVideo,
    path: 'conference-records',
  },
]);
</script>

<style scoped lang="scss">


  .content-view {
    overflow: hidden;
    flex: 1;
    display: flex;

    .toolbar {
      width: 200px;
      background: #141d34;
    }

    .main-panel-box {
      display: flex;
      flex-direction: column;
      flex: 1;
      padding: 20px;
      background: #253047;

      .title {
        color: #fff;
        font-size: 24px;
        font-weight: 600;
      }

      .content {
        margin: 20px;
        flex: 1;
        overflow: hidden;
      }
    }
  }
</style>