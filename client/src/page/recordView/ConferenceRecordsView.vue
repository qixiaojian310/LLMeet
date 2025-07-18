<template>
  <Toolbar class="conference-toolbar">
    <template #start>
      <InputText
        v-model="searchKeyword"
        placeholder="Search by title"
        @keyup.enter="filterConferences"
        class="search-input"
      />
    </template>
    <template #end>
      <Button icon="pi pi-refresh" label="Refresh" @click="loadConferences" />
    </template>
  </Toolbar>

  <div class="conference-records" v-if="conferences && conferences.length > 0">
    <Card v-for="conference in conferences" :key="conference.meeting_id" class="conference-record">
      <template #header>
        <div class="title">
          <div class="left">
            <FontAwesomeIcon :icon="faVideo" />
            <span>Record</span>
            <p class="description">Conference ID: {{ conference.meeting_id }}</p>
          </div>
          <Tag :value="conference.status" :severity="getStatusSeverity(conference.status)" />
        </div>
      </template>

      <template #content>
        <div class="conference-content">
          <div class="conference-info">
            <h3 class="conference-title">Conference title: {{ conference.title }}</h3>
          </div>
          <div class="conference-control">
            <div class="time-info">
              <div class="time-item">
                <FontAwesomeIcon :icon="faClock" />
                <span>{{ formatDateTime(conference.start_time) }}</span>
              </div>
              <div class="time-item">
                <FontAwesomeIcon :icon="faHourglassEnd" />
                <span>{{ formatDuration(conference.start_time, conference.end_time) }}</span>
              </div>
            </div>
            <div class="btn-group">
              <Button
                :disabled="
                  conference.meeting_id === recordStore.meeting_id && recordStore.isRecording
                "
                class="toolbar-button"
                severity="info"
                @click="redirect(conference.meeting_id)"
              >
                <span
                  v-if="conference.meeting_id === recordStore.meeting_id && recordStore.isRecording"
                >
                  <FontAwesomeIcon :icon="faSync" spin /> Stop
                </span>
                <span v-else> <FontAwesomeIcon :icon="faPlay" /> Play </span>
              </Button>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
  <div class="empty-box" v-else>
    <Empty
      :image="emptyRecordURL"
      :image-style="{
        height: '260px'
      }"
    >
      <template #description>
        <span> No meeting record </span>
      </template>
    </Empty>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faPlay,
  faVideo,
  faHourglassEnd,
  faClock,
  faSync
} from '@fortawesome/free-solid-svg-icons';
import { Card, Button, Tag, Toolbar, InputText } from 'primevue';
import { ref } from 'vue';
import { router } from '@/router';
import { onMounted } from 'vue';
import { getAllMeetingListWithRecordByUsername } from '@/request/meeting';
import { useRecordStore } from '@/stores/recordStore';
import { Empty } from 'ant-design-vue';

const emptyRecordURL = new URL('@/assets/loss/no_record.svg', import.meta.url).href;
const recordStore = useRecordStore();
interface Conference {
  meeting_id: string;
  title: string;
  description: string;
  start_time: string;
  end_time: string;
  endedAt: string;
  created_at: string;
  status: string;
  participants?: number[];
}

const conferences = ref<Conference[]>([]);
const searchKeyword = ref('');
const allConferences = ref<Conference[]>([]);

const loadConferences = async () => {
  const res = await getAllMeetingListWithRecordByUsername();
  if (typeof res !== 'number' && res.meetings) {
    allConferences.value = res.meetings;
    filterConferences();
  }
};

const filterConferences = () => {
  const keyword = searchKeyword.value.toLowerCase();
  conferences.value = allConferences.value.filter(conf =>
    conf.title.toLowerCase().includes(keyword)
  );
};
const formatDateTime = (dateString: string) => {
  const date = new Date(dateString);
  return date
    .toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
    .replace(/\//g, '-');
};

const formatDuration = (start: string, end: string) => {
  const startDate = new Date(start);
  const endDate = new Date(end);
  const duration = (endDate.getTime() - startDate.getTime()) / (1000 * 60);
  return `${Math.round(duration)} min`;
};

const getStatusSeverity = (status: string) => {
  switch (status.toLowerCase()) {
    case 'ready':
      return 'success';
    case 'ended':
      return 'info';
    case 'processing':
      return 'warning';
    default:
      return 'secondary';
  }
};

const redirect = (meeting_id: string) => {
  router.push({ name: 'ConferenceRecord', params: { meeting_id } });
};

onMounted(async () => {
  await loadConferences();
});
</script>

<style scoped lang="scss">
.conference-records {
  height: 100%;
  width: 100%;
  display: grid;
  /* 两列，每列等分宽度 */
  grid-template-columns: repeat(2, 1fr);
  /* 行列间距 */
  gap: 16px;
  /* 可选：左右内边距 */
  padding: 16px;
  overflow: auto;
  padding: 10px;

  .conference-record {
    width: 100%;
    height: fit-content;
    background: #ffffff;
    border: 1px solid var(--surface-border);
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    padding: 20px;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }

    .title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 1rem;
      font-weight: 600;
      color: var(--text-color);

      .left {
        display: flex;
        align-items: center;
        gap: 10px;

        svg {
          font-size: 1.2rem;
          color: var(--primary-color);
        }
      }
    }

    .conference-content {
      display: flex;
      gap: 0.3rem;
      flex-direction: column;
      .conference-info {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        width: 100%;
        .conference-title {
          font-size: 1.2rem;
          margin: 0;
          color: var(--text-color);
        }

        .description {
          color: var(--text-secondary-color);
          font-size: 0.95rem;
          margin: 0;
        }
      }
      .conference-control {
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
        font-size: 0.9rem;
        color: var(--text-secondary-color);
        .time-info {
          display: flex;
          flex-direction: column;
          gap: 0.3rem;
          flex-wrap: wrap;
          font-size: 0.9rem;
          color: var(--text-secondary-color);

          .time-item {
            display: flex;
            align-items: center;
            gap: 6px;
          }
        }
        .btn-group {
          display: flex;
          justify-content: flex-end;
          flex: 1;
          margin-left: 2rem;
        }
      }
    }
  }
}
</style>
<style lang="scss">
.conference-records {
  .p-card-body {
    padding: 20px 20px 0 20px !important;
  }
}
.empty-box {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
