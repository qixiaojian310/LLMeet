<template>
  <div class="main-panel">
    <div
      class="main-panel-header"
      :style="{ background: `url(${bgURL}) no-repeat center center`, backgroundSize: '100% auto' }"
    >
      <div class="main-panel-header-next-meet">
        <p>Upcoming Meeting at {{ meetingTime }}</p>
      </div>
      <div class="main-panel-header-time">
        <p class="time">
          {{ nowTime.time }}
        </p>
        <p class="date">
          {{ nowTime.date }}
        </p>
      </div>
    </div>
    <div class="meeting-tool">
      <Card v-for="tool in tools" :key="tool.title" @click="redirect(tool.path)">
        <template #header>
          <div
            :style="{
              background: `url(${tool.photo}) no-repeat center center`,
              backgroundSize: '100% auto'
            }"
            alt="Meeting Photo"
            class="meeting-photo"
          />
        </template>
        <template #content>
          <div class="content">
            <div class="icon">
              <FontAwesomeIcon :icon="tool.icon" />
            </div>
            <div class="text">
              <p class="title">
                {{ tool.title }}
              </p>
              <p class="description">
                {{ tool.description }}
              </p>
            </div>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card } from 'primevue';
import { ref, onMounted, onUnmounted } from 'vue';
import { ToolCardItem } from '@/types/mainLayout/toolbar';
import { faPlus, faUser, faVideo } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { router } from '@/router';
const meetingTime = ref(
  new Date(new Date().getTime() + 3 * 60 * 60 * 1000)
    .toISOString()
    .replace('T', ' ')
    .substring(0, 19)
);

const nowTime = ref({
  date: '',
  time: ''
});

const updateNowTime = () => {
  const dateObj = new Date();
  const datePart = dateObj.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  const timePart = dateObj.toTimeString().split(' ')[0];
  nowTime.value = {
    date: datePart,
    time: timePart
  };
};

let timer: ReturnType<typeof setInterval>;

const bgURL = ref(new URL('@/assets/main-bg.jpg', import.meta.url).href);

const tools = ref<ToolCardItem[]>([
  {
    title: 'New Meeting',
    icon: faPlus,
    photo: new URL('@/assets/card/meeting.jpg', import.meta.url).href,
    description: 'Create a new meeting',
    path: 'meeting-schedule-form'
  },
  {
    title: 'Join Meeting',
    icon: faUser,
    photo: new URL('@/assets/card/join.jpg', import.meta.url).href,
    description: 'Join a meeting',
    path: 'meeting-join-form'
  },
  {
    title: 'View Record',
    icon: faVideo,
    photo: new URL('@/assets/card/record.jpg', import.meta.url).href,
    description: 'View meeting record',
    path: 'conference-records'
  }
]);

const redirect = (path: string) => {
  router.push({ path: `/home/${path}` });
};

onMounted(() => {
  updateNowTime();
  timer = setInterval(updateNowTime, 1000); // 每秒更新一次
});

onUnmounted(() => {
  clearInterval(timer); // 防止内存泄漏
});
</script>

<style scoped lang="scss">
@use 'sass:math';
$scrollbar-width: 4px;

.main-panel {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;

  .main-panel-header {
    width: 100%;
    height: 200px;
    display: flex;
    border-radius: 10px;
    position: relative;

    .main-panel-header-next-meet {
      font-size: 5px;
      font-weight: 300;
      position: absolute;
      top: 20px;
      left: 20px;
      border-radius: 5px;
      background: #00000022;
      padding: 5px;

      p {
        padding: 0px;
        font-size: 10px;
        line-height: 10px;
        margin: 0;
      }
    }

    .main-panel-header-time {
      font-size: 5px;
      font-weight: 300;
      position: absolute;
      bottom: 20px;
      left: 20px;

      p {
        margin: 0 0 5px 0;
      }

      .time {
        text-align: left;
        font-size: 50px;
        font-weight: 600;
      }

      .date {
        font-size: 15px;
        text-align: left;
      }
    }
  }

  .meeting-tool {
    flex: 1;
    height: 0;
    width: 100%;
    overflow: auto;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;

    /* 整个滚动条 */
    &::-webkit-scrollbar {
      width: $scrollbar-width;
      /* 垂直滚动条宽度 */
      height: $scrollbar-width;
      /* 水平滚动条高度 */
    }

    /* 滚动条轨道（背景） */
    &::-webkit-scrollbar-track {
      background: #f0f0f0;
      border-radius: math.div($scrollbar-width, 2);
    }

    /* 滚动条滑块（thumb） */
    &::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: math.div($scrollbar-width, 2);
    }

    /* 滑块悬停时 */
    &::-webkit-scrollbar-thumb:hover {
      background: #555;
    }

    .p-card {
      border-radius: 10px;
      width: 230px;
      height: 200px;

      .meeting-photo {
        width: 100%;
        height: 100px;
        border-radius: 10px 10px 0 0;
      }

      .content {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .icon svg {
          background: #ffffff22;
          padding: 10px;
          border-radius: 5px;
        }

        .text {
          p {
            margin: 0;
          }

          .title {
            font-size: 15px;
            font-weight: 600;
          }

          .description {
            font-size: 10px;
            font-weight: 300;
          }
        }
      }
    }
  }
}
</style>
