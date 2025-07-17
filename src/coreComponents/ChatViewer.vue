<template>
  <div class="chat-container">
    <!-- 聊天框 -->
    <div class="chat-box" ref="chatBox">
      <!-- 已完成的消息 -->
      <AgentChatMessage
        v-for="(msg, idx) in chatLog"
        :key="idx"
        :message="msg.content"
        :isBot="msg.role === 'assistant'"
        :done="msg.done !== false"
      />

      <!-- 正在流式更新的最后一条消息 -->
      <AgentChatMessage
        v-if="lastMessage"
        :message="lastMessage.content"
        :isBot="true"
        :done="lastMessage.done"
      />
    </div>

    <!-- 输入框区域 -->
    <div class="chat-input-area">
      <Textarea
        v-model="userInput"
        rows="2"
        autoResize
        placeholder="Type your message..."
        @keyup.enter="onSend"
        class="chat-input"
      />
      <Button label="Send" icon="pi pi-send" @click="onSend" :disabled="loading" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { getChatStream } from '@/request/meeting';
import AgentChatMessage from './AgentChatMessage.vue';
import { Button, Textarea } from 'primevue';

const chatLog = ref([
  {
    role: 'assistant',
    content: 'Ask anything about your meeting.'
  }
]);
const lastMessage = ref(null);
const userInput = ref('');
const loading = ref(false);
const props = defineProps({
  segments: {
    type: Array,
    required: true
  },
  video_summarization: {
    type: String,
    required: true
  }
});
async function onSend() {
  const message = userInput.value.trim();
  if (!message || loading.value) return;

  // 推入用户消息
  chatLog.value.push({ role: 'user', content: message });

  // 清空输入、标记 loading，并初始化 lastMessage
  userInput.value = '';
  loading.value = true;
  lastMessage.value = { role: 'assistant', content: '', done: false };

  // 发起流式请求
  const resp = await getChatStream(
    chatLog.value.filter(m => m.role !== 'system'),
    props.segments,
    props.video_summarization
  );

  if (!resp.ok) {
    console.error(await resp.text());
    loading.value = false;
    lastMessage.value = null;
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  // 逐块读取、解析 SSE
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split('\n\n');
    buffer = parts.pop(); // 最后一段可能不完整

    for (const part of parts) {
      if (!part.startsWith('data:')) continue;
      const payload = part.replace(/^data:\s*/, '');
      if (payload === '[DONE]') {
        // 流结束：合并到 chatLog 并清空 lastMessage
        lastMessage.value.done = true;
        chatLog.value.push(lastMessage.value);
        lastMessage.value = null;
        loading.value = false;
        return;
      }
      try {
        const obj = JSON.parse(payload);
        const delta = obj.choices?.[0]?.delta?.content;
        if (delta) {
          lastMessage.value.content += delta;
        }
      } catch (e) {
        console.warn('parse SSE chunk failed', e);
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  font-size: 0.85rem;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chat-input-area {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
  border-radius: 10px;
  width: 100%;
  .chat-input {
    flex: 1;
  }
}
</style>
