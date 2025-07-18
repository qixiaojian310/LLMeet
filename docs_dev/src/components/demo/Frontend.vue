<template>
  <DemoView :events="events" :details="details"/>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DemoView from './DemoView.vue';

const events = ref([
  {
    status: 'Design init',
    date: '2025-03-15',
    color: '#9C27B0',
    text: 'Completed the initial UI design, including the layout for the meeting interface, button styles, and color scheme.',
  },
  {
    status: 'Use Tauri init',
    date: '2025-03-20',
    color: '#673AB7',
    text: 'Initialized the Tauri project and set up the cross-platform desktop app foundation, enabling communication between frontend and system layers.',
  },
  {
    status: 'Create basic layout',
    date: '2025-04-01',
    color: '#FF9800',
    text: 'Built the core application layout, including the top navigation bar, video display area, and control panel structure.',
  },
  {
    status: 'Finish frontend startup',
    date: '2025-04-05',
    color: '#607D8B',
    text: 'Implemented camera access using the MediaDevices API and completed the initial frontend startup flow, establishing basic communication with the backend.',
  },
  {
    status: 'Finish HTTP Wrapper',
    date: '2025-05-05',
    color: '#607D8B',
    text: 'Used Tauri and Rust to wrap HTTP/HTTPS requests on the client side, improving security and avoiding CORS issues in cross-origin communication.',
  },
  {
    status: 'Update theme colors',
    date: '2025-05-20',
    color: '#3F51B5',
    text: 'Refactored the UI theme to support custom colors and light/dark modes, enhancing visual consistency across the application.',
  },
  {
    status: 'Add loading and empty states',
    date: '2025-06-01',
    color: '#00BCD4',
    text: 'Introduced comprehensive loading indicators and empty state components throughout the app to improve user feedback and perceived performance.',
  },
  {
    status: 'Integrate WebRTC frontend',
    date: '2025-06-10',
    color: '#4CAF50',
    text: 'Connected the frontend interface with the underlying WebRTC engine, enabling real-time video and audio communication within the meeting interface.',
  },
  {
    status: 'Add recording UI',
    date: '2025-06-20',
    color: '#F44336',
    text: 'Designed and implemented the recording interface, including visual indicators for active recording and user guidance during the session.',
  },
  {
    status: 'Implement video buffering (video.js)',
    date: '2025-07-05',
    color: '#9E9E9E',
    text: 'Integrated video.js and developed a custom buffering module to support synchronized playback of multi-source meeting recordings.',
  },
  {
    status: 'Connect LLM via SSE',
    date: '2025-07-15',
    color: '#2196F3',
    text: 'Established an SSE connection to the LLM backend, enabling real-time assistant responses and streaming output in the chatbot interface.',
  },
]);

const details = ref([
    {
      path: new URL('@/assets/frontend/f-1.png', import.meta.url).href,
      description: 'Login',
    },
    {
      path: new URL('@/assets/frontend/f-2.png', import.meta.url).href,
      description: 'Register',
    },
    {
      path: new URL('@/assets/frontend/f-3.png', import.meta.url).href,
      description: 'Home',
    },
    {
      path: new URL('@/assets/frontend/f-4.png', import.meta.url).href,
      description: 'Create Meeting',
    },
    {
      path: new URL('@/assets/frontend/f-5.png', import.meta.url).href,
      description: 'Join Meeting',
    },
    {
      path: new URL('@/assets/frontend/f-6.png', import.meta.url).href,
      description: 'Meeting',
    },
    {
      path: new URL('@/assets/frontend/f-7.png', import.meta.url).href,
      description: 'Meeting information',
    },
    {
      path: new URL('@/assets/frontend/f-8.png', import.meta.url).href,
      description: 'Meeting Record List',
    },
    {
      path: new URL('@/assets/frontend/f-9.png', import.meta.url).href,
      description: 'Meeting Record With Transcript',
    },
    {
      path: new URL('@/assets/frontend/f-10.png', import.meta.url).href,
      description: 'Meeting Record With Summarization',
    },
    {
      path: new URL('@/assets/frontend/f-11.png', import.meta.url).href,
      description: 'Meeting Record With Chatbot',
    },
    {
      path: new URL('@/assets/frontend/f-12.png', import.meta.url).href,
      description: 'Schedule',
    },
    {
      path: new URL('@/assets/frontend/f-13.png', import.meta.url).href,
      description: 'Schedule Item',
    },
])
</script>

<style scoped></style>