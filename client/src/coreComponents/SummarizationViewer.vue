<template>
  <div class="summary-container">
    <!-- 输入按钮触发摘要 -->
    <Toolbar>
      <template #end>
        <Button @click="startSummarization">Refresh</Button>
      </template>
    </Toolbar>
    <!-- 渲染 Markdown 转 HTML -->
    <div v-html="renderedHtml" class="markdown-body"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { marked } from 'marked';
import { getSummary } from '@/request/meeting';
import { Button, Toolbar } from 'primevue';

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

// 1. 存放从后端累计的纯文本 Markdown
const renderedMd = ref('');

// 2. 将 Markdown 转 HTML
const renderedHtml = computed(() => marked.parse(renderedMd.value));

// 4. 拉取流式数据并累积
async function startSummarization() {
  renderedMd.value = ''; // 重置
  const resp = await getSummary(props.segments, props.video_summarization);
  if (!resp.ok) {
    console.error(await resp.text());
    return;
  }
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // SSE 数据块以 "\n\n" 分隔
    const parts = buffer.split('\n\n');
    buffer = parts.pop(); // 最后一段可能还不完整，留到下次解析
    for (const part of parts) {
      // 每块通常是 "data: {...}"
      if (!part.startsWith('data:')) continue;
      const payload = part.replace(/^data:\s*/, '');
      if (payload === '[DONE]') {
        reader.cancel();
        return;
      }
      try {
        const obj = JSON.parse(payload);
        const delta = obj.choices?.[0]?.delta?.content;
        if (delta) {
          // 累积到 renderedMd
          renderedMd.value += delta;
        }
      } catch (e) {
        // 忽略解析错误
        console.warn('parse SSE chunk failed', e);
      }
    }
  }
}

onMounted(() => {
  startSummarization();
});
</script>

<style scoped>
.summary-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}
/* 如果你想让 GitHub 样式更舒服，可以引入一个 markdown CSS */
.markdown-body {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
}
</style>
