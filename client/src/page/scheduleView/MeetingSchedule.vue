<template>
  <FullCalendar :options="calendarOptions" />
  <Dialog v-model:visible="visible" modal header="Meeting Details" :style="{ width: '30rem' }">
    <template #default>
      <div v-if="clickEvent">
        <h3>{{ clickEvent.title }}</h3>
        <p><strong>Description:</strong> {{ clickEvent.extendedProps.description }}</p>
        <p><strong>Start Time:</strong> {{ formatDate(clickEvent.start) }}</p>
        <p><strong>End Time:</strong> {{ formatDate(clickEvent.end) }}</p>
        <p><strong>Created By:</strong> {{ clickEvent.extendedProps.creator_id }}</p>
        <p><strong>Status:</strong> {{ clickEvent.extendedProps.status }}</p>
        <p><strong>Meeting ID:</strong> {{ clickEvent.extendedProps.meeting_id }}</p>
      </div>
    </template>
    <template #footer>
      <Button type="button" label="Close" severity="secondary" @click="visible = false" />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Dialog, Button } from 'primevue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import { CalendarOptions } from '@fullcalendar/core/index.js';
import { getAllMeetingListByUsername } from '@/request/meeting';
import { message } from 'ant-design-vue';
import { EventImpl } from '@fullcalendar/core/internal';
import dayjs from '@/utils/dayjsUtils';

const clickEvent = ref<EventImpl | null>(null);

const formatDate = (date: Date | string | null) => {
  if (!date) return '';
  return dayjs(date).format('YYYY-MM-DD HH:mm');
};
const visible = ref(false);
const calendarOptions = ref<CalendarOptions>({
  plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
  expandRows: true,
  height: '100%',

  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  initialView: 'timeGridWeek',
  navLinks: true, // can click day/week names to navigate views
  editable: false,
  selectable: true,
  nowIndicator: true,
  dayMaxEvents: true,
  eventClick: info => {
    info.jsEvent.preventDefault(); // don't let the browser navigate
    clickEvent.value = info.event;
    visible.value = true;
  }
});
onMounted(async () => {
  const getAllRes = await getAllMeetingListByUsername();
  if (typeof getAllRes !== 'number' && getAllRes.meetings) {
    calendarOptions.value = {
      ...calendarOptions.value,
      events: getAllRes.meetings.map((meeting: any) => {
        return {
          title: meeting.title,
          start: meeting.start_time,
          end: meeting.end_time,
          description: meeting.description,
          creator_id: meeting.creator_id,
          status: meeting.status,
          meeting_id: meeting.meeting_id
        };
      })
    };
  } else {
    message.error('Failed to fetch meetings');
  }
});
</script>
<style lang="scss">
.fc-timegrid-event-harness {
  &:hover {
    cursor: pointer;
  }
}
</style>
