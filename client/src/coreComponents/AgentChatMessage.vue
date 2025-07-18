<template>
  <div class="message" :class="isBot ? 'bot-message' : 'human-message'">
    <div class="avatar">
      <FontAwesomeIcon v-if="isBot" :icon="faRobot" />
      <FontAwesomeIcon v-else :icon="faUser" />
    </div>

    <div class="message-content">
      <div v-if="message" ref="containerRef" class="chat-markdown" v-html="renderedHtml"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { marked } from 'marked';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUser, faRobot } from '@fortawesome/free-solid-svg-icons';

const props = defineProps({
  message: String,
  isBot: Boolean,
  done: Boolean
});

const containerRef = ref(null);
const renderedHtml = ref('');

onMounted(async () => {
  renderedHtml.value = await marked.parse(props.message || '');
});

watch(
  () => props.message,
  async val => {
    renderedHtml.value = await marked.parse(val || '');
  }
);
</script>

<style scoped>
.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  gap: 10px;
}

.avatar {
  font-size: 1.5rem;
  color: #4e73df;
}

.message-content {
  background: #f1f5ff;
  padding: 10px 15px;
  border-radius: 8px;
  max-width: 100%;
  color: #1a2347;
}

.message.human-message {
  flex-direction: row-reverse;
}

.message.human-message .message-content {
  background: linear-gradient(135deg, #0095ff, #0055cc);
  color: #fff;
}

.chat-markdown a {
  color: #1976d2;
  text-decoration: underline;
}

.flow-status {
  margin-bottom: 4px;
}

.flow-event {
  display: flex;
  align-items: center;
  margin-right: 12px;
}

.flow-name {
  font-weight: 500;
  margin-right: 2px;
}

.flow-status-text {
  text-transform: capitalize;
}

.loading {
  font-weight: bold;
  animation: loadingWave 1.5s infinite;
}

.dot {
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%,
  100% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
}
</style>
