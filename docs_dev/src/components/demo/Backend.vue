<template>
  <DemoView :events="events" :details="details"/>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DemoView from './DemoView.vue';

const events = ref([
  {
    status: 'Design UML',
    date: '2025-03-15',
    color: '#9C27B0',
    text: 'Outlined system architecture and user flow using UML diagrams.',
  },
  {
    status: 'Design database',
    date: '2025-03-20',
    color: '#673AB7',
    text: 'Defined database schema and relationships for user and meeting data.',
  },
  {
    status: 'JWT',
    date: '2025-04-01',
    color: '#FF9800',
    text: 'Integrated JSON Web Token for secure user authentication.',
  },
  {
    status: 'Login and registers',
    date: '2025-04-05',
    color: '#607D8B',
    text: 'Developed login and registration interfaces with form validation.',
  },
  {
    status: 'Meeting',
    date: '2025-04-25',
    color: '#009688',
    text: 'Implemented meeting creation, scheduling, and management, we start a meeting management in database and backend',
  }
]);


const details = ref([
    {
      path: new URL('@/assets/backend/b-1.png', import.meta.url).href,
      description: 'UML',
    },
    {
      path: new URL('@/assets/backend/b-2.png', import.meta.url).href,
      description: 'JWT',
    },
    {
      path: new URL('@/assets/backend/b-3.png', import.meta.url).href,
      description: 'Login and registers',
    },
    {
      path: new URL('@/assets/backend/b-4.png', import.meta.url).href,
      description: 'Meeting management',
    }
])
</script>

<style scoped></style>