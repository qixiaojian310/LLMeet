<template>
  <FullCalendar :options="calendarOptions" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';

const calendarOptions = ref({
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
  editable: true,
  selectable: true,
  nowIndicator: true,
  dayMaxEvents: true // allow "more" link when too many events
});
</script>
