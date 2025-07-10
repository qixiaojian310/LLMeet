<template>
  <div class="main-panel">
    <div class="meeting-tool">
      <Card v-for="tool in tools" :key="tool.title" @click="redirect(tool.path)">
        <template #header>
          <div class="meeting-title">
            <div class="icon">
              <FontAwesomeIcon :icon="tool.icon" size="2x" />
            </div>
            <div
              :style="{
                background: `url(${tool.photo}) no-repeat center center`,
                backgroundSize: '100% auto'
              }"
              alt="Meeting Photo"
              class="meeting-photo"
            />
          </div>
        </template>
        <template #content>
          <div class="content">
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
    <div class="main-panel-header">
      <div class="main-panel-header-time">
        <p class="time">
          {{ nowTime.time }}
        </p>
        <p class="date">
          {{ nowTime.date }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card } from 'primevue';
import { ref, onMounted, onUnmounted } from 'vue';
import { ToolCardItem } from '@/types/mainLayout/toolbar';
import { faPlus, faTimeline, faUser, faVideo } from '@fortawesome/free-solid-svg-icons';
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
  },
  {
    title: 'Schedule',
    icon: faTimeline,
    photo: new URL('@/assets/card/schedule.jpg', import.meta.url).href,
    description: 'View meeting schedule',
    path: 'schedule'
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
  gap: 20px;

  .main-panel-header {
    flex: 1;
    width: 0%;
    display: flex;
    border-radius: 10px;
    position: relative;
    flex-direction: column;
    .main-panel-header-time {
      display: flex;
      flex-direction: column;
      height: fit-content;
      width: 100%;
      p {
        margin: 0 0 5px 0;
      }

      .time {
        text-align: left;
        font-size: 3rem;
        font-weight: 600;
        line-height: 1.2;
      }

      .date {
        font-size: 1.2rem;
        text-align: left;
      }
    }
  }

  .meeting-tool {
    flex: 0;
    height: 100%;
    min-width: 350px;
    overflow: auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr); // 2列
    grid-auto-rows: minmax(150px, auto); // 自适应行高
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
    .p-card:nth-child(-n + 2) {
      align-self: end;
    }
    .p-card {
      border-radius: 10px;
      width: 100%;
      height: 120px;
      .meeting-title {
        display: flex;
        .meeting-photo {
          flex: 1;
          height: 50px;
          border-radius: 0px 10px 0 0;
        }
        .icon svg {
          background: #ffffff22;
          padding: 10px;
          border-radius: 5px;
        }
      }

      .content {
        display: flex;
        justify-content: space-between;
        align-items: center;

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
