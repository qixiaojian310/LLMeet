<template>
  <div class="content-view">
    <div class="toolbar">
      <Toolbar :buttons="navigationItems" />
    </div>
    <div class="main-panel-box">
      <div class="title">
        {{ router.currentRoute.value.meta.title }}
      </div>
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Toolbar from '@/coreComponents/Toolbar.vue';
import { faFileVideo, faHouse, faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import { router } from '@/router';

const navigationItems = ref([
  {
    title: 'Home',
    icon: faHouse,
    path: ''
  },
  {
    title: 'Join Conference',
    icon: faSquarePlus,
    path: 'meeting-join-form'
  },
  {
    title: 'Records',
    icon: faFileVideo,
    path: 'conference-records'
  }
]);
</script>

<style scoped lang="scss">
.content-view {
  overflow: hidden;
  flex: 1;
  display: flex;

  .toolbar {
    width: 150px;
    background: var(--primary-background-color);
    position: relative;
    z-index: 10;
  }

  .main-panel-box {
    position: relative;
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 20px;
    background: var(--secondary-background-color);

    .title {
      color: var(--primary-text-color);
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
