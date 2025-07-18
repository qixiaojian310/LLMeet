<template>
  <DemoView :events="events" :details="details"/>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DemoView from './DemoView.vue';

const events = ref([
  {
    status: 'Register a Domain',
    date: '2025-04-15',
    color: '#9C27B0',
    text: 'We have already register a domain name for our project, which is hkucompcs.xyz',
  },
  {
    status: 'get a SSL certificate',
    date: '2025-04-20',
    color: '#673AB7',
    text: 'We use Let\'s Encrypt to get a SSL certificate for our domain name, so you can use https://hkucompcs.xyz to see it',
  },
  {
    status: 'Deploy Livekit',
    date: '2025-04-20',
    color: '#FF9800',
    text: 'We consider use Livekit to deploy our project, which is a open source video conferencing solution, it is easy to use but it need https, so we prepare these services',
  },
  {
    status: 'Refresh HKUCS Webpage',
    date: '2025-05-05',
    color: '#607D8B',
    text: 'Except the website in github, we also refresh the HKUCS webpage to show our project',
  },
  {
    status: 'Deploy a model',
    date: '2025-07-05',
    color: '#607D8B',
    text: 'We use fastapi to deploy our model, and use nginx to reverse proxy the request from AI server to a server which have independent IP Address',

  },
]);


const details = ref([
    {
      path: new URL('@/assets/deployment/d-1.png', import.meta.url).href,
      description: 'Domain Preparation',
    },
    {
      path: new URL('@/assets/deployment/d-2.png', import.meta.url).href,
      description: 'SSL Certificate',
    },
    {
      path: new URL('@/assets/deployment/d-3.png', import.meta.url).href,
      description: 'Livekit prerequisites',
    },
    
])
</script>

<style scoped></style>