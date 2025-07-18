<template>
  <DemoView :events="events" :details="details"/>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DemoView from './DemoView.vue';

const events = ref([
  {
    status: 'Attempt fine-tuning model',
    date: '2025-04-01',
    color: '#9C27B0',
    text: 'Initiated initial attempts at fine-tuning the base language model with meeting-related data.',
  },
  {
    status: 'Load fine-tuning model',
    date: '2025-04-03',
    color: '#673AB7',
    text: 'Successfully loaded the fine-tuned model with LoRA adapters and verified model readiness for inference.',
  },
  {
    status: 'fine-tuning model wtih CNNDM',
    date: '2025-04-27',
    color: '#FF9800',
    text: 'Fine-tuned the model using the CNNDM dataset, achieving promising results in meeting summarization, not just in meeting summarization, but also in other text.',
  },
  {
    status: 'fine-tuning model wtih MeetingBank',
    date: '2025-05-05',
    color: '#009688',
    text: 'Fine-tuned the Task-Oriented Dialog Summarization dataset, achieving promising results in meeting summarization, not just in meeting summarization, but also in other text.',
  }
]);


const details = ref([
    {
      path: new URL('@/assets/model/m-1.png', import.meta.url).href,
      description: 'Adapt LoRA',
    },
    {
      path: new URL('@/assets/model/m-2.png', import.meta.url).href,
      description: 'Load LoRA Adapter',
    },
])
</script>

<style scoped></style>