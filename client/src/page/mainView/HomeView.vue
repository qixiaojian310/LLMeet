<template>
  <div class="main-panel">
    <div class="meeting-tool">
      <Card
        class="meeting-nav-card"
        v-for="tool in tools"
        :key="tool.title"
        @click="redirect(tool.path)"
      >
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
    <Divider layout="vertical" style="margin: 0" />
    <div class="main-panel-header">
      <div class="main-panel-header-time">
        <p class="subdate">
          {{ nowTime.fullDate }}
        </p>
        <div class="smalldate">
          <p class="date">
            {{ nowTime.date }}
          </p>
          <p class="time">
            {{ nowTime.time }}
          </p>
        </div>
      </div>
      <Divider />
      <div class="schedule-list" v-if="meetings && meetings.length > 0">
        <div class="schedule-item" v-for="meeting in meetings" :key="meeting.meeting_id">
          <div class="title">
            <p>{{ meeting.title }}</p>
            <p>{{ dateConverter(meeting.start_time) }}</p>
          </div>
          <div class="schedule-item-content">
            <p class="time">
              {{ timeConverter(meeting.start_time) }}-{{ timeConverter(meeting.end_time) }}
            </p>
            <span class="room">Room: {{ meeting.meeting_id }}</span>
            <div class="schedule-item-btn-group">
              <Button label="Join" @click="joinMeetingHandler(meeting)" />
              <Button @click="deleteMeetingHandler(meeting)" severity="danger">
                <FontAwesomeIcon :icon="faTrash" />
              </Button>
            </div>
          </div>
        </div>
      </div>
      <div class="empty-box" v-else>
        <Empty
          :image="emptyMeetingURL"
          :image-style="{
            height: '260px'
          }"
        >
          <template #description>
            <span> No meeting record </span>
          </template>
        </Empty>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card, Divider, Button } from 'primevue';
import { ref, onMounted, onUnmounted } from 'vue';
import { ToolCardItem } from '@/types/mainLayout/toolbar';
import { faPlus, faTimeline, faTrash, faUser, faVideo } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { router } from '@/router';
import {
  deleteMeeting,
  getAllMeetingListByUsername,
  getMeetingToken,
  startBot
} from '@/request/meeting';
import { Meeting } from '@/types/model/meeting';
import { useUserStore } from '@/stores/userStore';
import { Empty, message } from 'ant-design-vue';
import { useMeetingStore } from '@/stores/meetingStore';
import { useRecordStore } from '@/stores/recordStore';
import dayjs from '@/utils/dayjsUtils';

const meetings = ref<Meeting[]>([]);
const emptyMeetingURL = new URL('@/assets/loss/no_meeting.svg', import.meta.url).href;
const timeConverter = (timeStr: string) => {
  return dayjs.utc(timeStr).tz(dayjs.tz.guess()).format('HH:mm');
};
const userStore = useUserStore();
const meetingStore = useMeetingStore();
const recordStore = useRecordStore();

const dateConverter = (timeStr: string) => {
  return dayjs.utc(timeStr).tz(dayjs.tz.guess()).format('YYYY-MM-DD');
};

const nowTime = ref({
  date: '',
  time: '',
  fullDate: ''
});

const updateNowTime = () => {
  const now = dayjs();

  nowTime.value = {
    date: now.format('dddd'), // e.g., "Wednesday"
    time: now.format('HH:mm:ss'), // e.g., "14:22:05"
    fullDate: now.format('MMMM D') // e.g., "July 10"
  };
};

let timer: ReturnType<typeof setInterval>;
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
    description: 'View record',
    path: 'conference-records'
  },
  {
    title: 'Schedule',
    icon: faTimeline,
    photo: new URL('@/assets/card/schedule.jpg', import.meta.url).href,
    description: 'View schedule',
    path: 'schedule'
  }
]);

const redirect = (path: string) => {
  router.push({ path: `/home/${path}` });
};

const joinMeetingHandler = async (meeting: Meeting) => {
  const tokenRes = await getMeetingToken(meeting.meeting_id, userStore.username);

  // 获取 token 失败，撤回会议
  if (typeof tokenRes === 'number') {
    message.error('Meeting token generation failed');
    const deleteRes = await deleteMeeting(meeting.meeting_id);
    if (deleteRes.success) {
      message.success('Meeting deleted successfully');
    }
    return;
  }

  // 启动 bot
  const startBotRes = await startBot(meeting.meeting_id);
  console.log(startBotRes);

  // 设置会议信息并跳转
  message.success('Meeting created successfully');
  meetingStore.setMeetingInfo({
    meeting_id: meeting.meeting_id,
    meetingToken: tokenRes.token,
    meetingName: meeting.title,
    description: meeting.description,
    start_time: meeting.start_time.slice(0, 19).replace('T', ' '),
    end_time: meeting.end_time.slice(0, 19).replace('T', ' '),
    create_time: new Date(meeting.start_time).toISOString().slice(0, 19).replace('T', ' ')
  });
  recordStore.recordVideo(meeting.meeting_id);
  router.push({ name: 'MeetingView' });
};

const deleteMeetingHandler = async (meeting: Meeting) => {
  const deleteRes = await deleteMeeting(meeting.meeting_id);
  if (deleteRes.success) {
    message.success('Meeting deleted successfully');
  }
  const getAllRes = await getAllMeetingListByUsername();
  if (getAllRes.success) {
    meetings.value = getAllRes.meetings;
  }
};

onMounted(async () => {
  updateNowTime();
  timer = setInterval(updateNowTime, 1000); // 每秒更新一次

  //获取所有的加入日程列表
  const res = await getAllMeetingListByUsername();
  if (res.success) {
    meetings.value = res.meetings;
  }
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

  .main-panel-header {
    flex: 1;
    width: 0%;
    display: flex;
    border-radius: 10px;
    position: relative;
    flex-direction: column;
    .main-panel-header-time {
      padding: 0 20px;
      display: flex;
      flex-direction: column;
      height: fit-content;
      width: 100%;
      p {
        margin: 0 0 5px 0;
      }
      .smalldate {
        display: flex;
        justify-content: space-between;
        .time {
          text-align: left;
          font-size: 1.2rem;
        }
        .date {
          text-align: left;
          font-size: 1.2rem;
          margin-bottom: 5px;
        }
      }
      .subdate {
        font-size: 3rem;
        font-weight: 600;
        line-height: 1.2;
        text-align: left;
      }
    }
    .schedule-list {
      flex: 1;
      padding: 20px 20px 0 20px;
      display: flex;
      flex-direction: column;
      overflow: hidden auto;
      gap: 1rem;
      p {
        margin: 0;
      }
      .schedule-item {
        display: flex;
        flex-direction: column;
        padding: 5px;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition:
          transform 0.2s ease,
          box-shadow 0.2s ease;
        .title {
          display: flex;
          gap: 1rem;
          position: relative;
          width: 100%;
        }
        .schedule-item-content {
          flex: 1;
          display: flex;
          gap: 1rem;
          color: var(--secondary-text-color);
          align-items: center;
          .schedule-item-btn-group {
            flex: 1;
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 0.5rem;
          }
        }
        &:hover {
          cursor: pointer;
          background: var(--schedule-item-background-color);
          transform: translateY(-5px); // 向上抬起 5px
          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); // 更强阴影
        }
      }
    }
    .empty-box {
      height: 100%;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }

  .meeting-tool {
    flex: 0;
    height: 100%;
    min-width: 300px;
    overflow: auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr); // 2列
    grid-auto-rows: minmax(150px, auto); // 自适应行高
    gap: 20px;
    padding-right: 20px;

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
    .meeting-nav-card {
      border-radius: 10px;
      width: 100%;
      height: 120px;
      transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); // 默认轻微阴影
      cursor: pointer;

      &:hover {
        transform: translateY(-5px); // 向上抬起 5px
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); // 更强阴影
      }
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
