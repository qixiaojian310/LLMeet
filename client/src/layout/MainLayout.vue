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
import { faFileVideo, faHouse, faSquarePlus, faTimeline } from '@fortawesome/free-solid-svg-icons';
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import { router } from '@/router';
import { useWSService } from '@/utils/useWSService';
import { message } from 'ant-design-vue';
import { useRecordStore } from '@/stores/recordStore';

const recordStore = useRecordStore();
const navigationItems = ref([
  {
    title: 'Home',
    icon: faHouse,
    path: ''
  },
  {
    title: 'Join',
    icon: faSquarePlus,
    path: 'meeting-join-form'
  },
  {
    title: 'Records',
    icon: faFileVideo,
    path: 'conference-records'
  },
  {
    title: 'Schedule',
    icon: faTimeline,
    path: 'schedule'
  }
]);

useWSService(event => {
  console.log('收到 merge_complete：', event);
  message.success('merge_complete!!');
  recordStore.stopRecord();
  // 你还可以触发通知、状态更新等
});
</script>

<style scoped lang="scss">
.content-view {
  overflow: hidden;
  flex: 1;
  display: flex;

  .toolbar {
    width: fit-content;
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
      margin: 1rem;
      flex: 1;
      overflow: hidden;
    }
  }
}
</style>
