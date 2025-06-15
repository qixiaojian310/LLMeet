<template>
  <div class="conference-records">
    <Card v-for="conference in conferences" class="conference-record" :key="conference.meetingId">
      <template #header>
        <div class="title">
          <FontAwesomeIcon :icon="fas.faVideo" />
          <div>Meeting Record</div>
          <Tag :value="conference.status" :severity="getStatusSeverity(conference.status)" />
        </div>
      </template>
      <template #content>
        <div class="conference-content">
          <div class="text">
            <h3>{{ conference.title }}</h3>
            <p class="description">{{ conference.description }}</p>
            <div class="time-info">
              <div class="time-item">
                <FontAwesomeIcon :icon="fas.faClock" />
                <span>{{ formatDateTime(conference.startTime) }}</span>
              </div>
              <div class="time-item">
                <FontAwesomeIcon :icon="fas.faHourglassEnd" />
                <span>{{ formatDuration(conference.startTime, conference.endTime) }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <div class="conference-footer">
          <AvatarGroup>
            <Avatar v-for="participant in conference.participants || []" 
                   :key="participant" 
                   shape="circle"
                   :label="participant.toString()" />
          </AvatarGroup>
          <Button severity="info" class="toolbar-button" @click="redirect(conference.meetingId)">
            <FontAwesomeIcon :icon="fas.faPlay" />
            Play
          </Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { Card, Avatar, AvatarGroup, Button, Tag } from 'primevue';
import { ref } from 'vue';
import { router } from '@/router';
import { onMounted } from 'vue';
import { getAllMeetingListByUserId } from '@/request/meeting';

interface Conference {
  meetingId: string;
  title: string;
  description: string;
  startTime: string;
  endTime: string;
  endedAt: string;
  createdAt: string;
  status: string;
  participants?: number[];
}

const conferences = ref<Conference[]>([]);

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).replace(/\//g, '-');
};

const formatDuration = (start: string, end: string) => {
  const startDate = new Date(start);
  const endDate = new Date(end);
  const duration = (endDate.getTime() - startDate.getTime()) / (1000 * 60);
  return `${Math.round(duration)} min`;
};

const getStatusSeverity = (status: string) => {
  switch (status.toLowerCase()) {
    case 'ready': return 'success';
    case 'ended': return 'info';
    case 'processing': return 'warning';
    default: return 'secondary';
  }
};

const redirect = (meetingId: string) => {
  router.push({ name: 'ConferenceRecord', params: { meetingId } });
};

onMounted(async () => {
  const res = await getAllMeetingListByUserId();
  if (typeof res !== 'number' && res.meetings) {
    conferences.value = res.meetings.map((meeting: any) => ({
      ...meeting,
      // 如果API没有返回participants，可以设置默认值或留空
      participants: meeting.participants || [1, 2, 3] // 示例数据，实际应从API获取
    }));
  }
});
</script>

<style scoped lang="scss">
.conference-records {
  height: 100%;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  overflow: auto;
  padding: 10px;

  .conference-record {
    width: 320px;
    height: fit-content;
    background: #00000011;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.2s, box-shadow 0.2s;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }

    .title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
      margin-bottom: 12px;
      
      > div {
        display: flex;
        align-items: center;
        gap: 8px;
      }
    }

    .conference-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      
      h3 {
        margin: 0 0 8px 0;
        font-size: 1.1rem;
        color: var(--text-color);
      }

      .description {
        color: var(--text-secondary-color);
        margin-bottom: 12px;
        font-size: 0.9rem;
      }

      .time-info {
        margin-top: auto;
        
        .time-item {
          display: flex;
          align-items: center;
          gap: 6px;
          margin-bottom: 6px;
          font-size: 0.85rem;
          color: var(--text-secondary-color);
        }
      }
    }

    .conference-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 16px;
      padding-top: 12px;
      border-top: 1px solid var(--surface-border);
    }
  }
}
</style>