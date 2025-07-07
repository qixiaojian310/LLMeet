<template>
  <div class="transcription-viewer">
    <div class="header">
      <h2>Transcription</h2>
      <span class="language">Language: {{ data.language.toUpperCase() }}</span>
    </div>
    <ul class="segments-list">
      <li v-for="(seg, index) in data.segments" :key="index" class="segment-item">
        <div class="segment-badge" :style="{ backgroundColor: getSpeakerColor(seg.speaker) }">
          {{ seg.speaker }}
        </div>
        <div class="segment-content">
          <div class="segment-time">{{ formatTime(seg.start) }} - {{ formatTime(seg.end) }}</div>
          <div class="segment-text">{{ seg.text }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

type Segment = { speaker: string; start: number; end: number; text: string };

interface TranscriptionData {
  language: string;
  segments: Segment[];
}

const props = defineProps<{ data: TranscriptionData }>();

// Generate a consistent color for each speaker
const speakerColors: Record<string, string> = {};
const palette = ['#FFB6C1', '#ADD8E6', '#90EE90', '#FFD700', '#FFA07A', '#DDA0DD'];
function getSpeakerColor(speaker: string): string {
  if (!speakerColors[speaker]) {
    const idx = Object.keys(speakerColors).length % palette.length;
    speakerColors[speaker] = palette[idx];
  }
  return speakerColors[speaker];
}

function formatTime(sec: number): string {
  const m = String(Math.floor(sec / 60)).padStart(2, '0');
  const s = String(Math.floor(sec % 60)).padStart(2, '0');
  return `${m}:${s}`;
}
</script>

<style scoped lang="scss">
.transcription-viewer {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background: #fafafa;
  overflow-y: auto;
  height: 100%;
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h2 {
      margin: 0;
      font-size: 1.5rem;
      color: #333;
    }
    .language {
      font-size: 0.9rem;
      color: #666;
    }
  }

  .segments-list {
    list-style: none;
    padding: 0;
    margin: 0;

    .segment-item {
      display: flex;
      align-items: flex-start;
      padding: 0.75rem;
      border-bottom: 1px solid #e0e0e0;
      transition: background 0.2s;

      &:hover {
        background: #f0f0f0;
      }

      .segment-badge {
        flex-shrink: 0;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-weight: bold;
        margin-right: 1rem;
      }

      .segment-content {
        flex: 1;

        .segment-time {
          font-size: 0.85rem;
          color: #999;
          margin-bottom: 0.25rem;
        }
        .segment-text {
          font-size: 1rem;
          color: #444;
          line-height: 1.4;
        }
      }
    }
  }
}
</style>
