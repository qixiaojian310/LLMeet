<template>
  <div class="conference-record">
    <div class="video-panel">
      <div v-if="videos.length" class="video-player">
        <div v-for="video in videos" class="video-item" :key="video.path">
          <div class="video-content">
            <p class="video-user">
              {{ video.username }}
            </p>
            <video class="video-js vjs-default-skin my-video" controls />
          </div>
        </div>
      </div>
      <div class="video-control">
        <button class="control-btn" @click="togglePlay">
          <FontAwesomeIcon :icon="isPlaying ? faPause : faPlay" />
        </button>
        <button class="control-btn" @click="seekRelative(-5)">
          <FontAwesomeIcon :icon="faBackward" />
        </button>
        <span class="time-display"
          >{{ formatTime(currentTime) }} / {{ formatTime(totalTime) }}</span
        >
        <div class="progress-bar" @click="onProgressClick">
          <div class="progress-filled" :style="{ width: globalProgress + '%' }"></div>
        </div>
        <button class="control-btn" @click="seekRelative(5)">
          <FontAwesomeIcon :icon="faForward" />
        </button>
        <div class="volume-control">
          <FontAwesomeIcon :icon="faVolumeUp" />
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            v-model.number="volume"
            @input="onVolumeChange"
          />
        </div>
        <button class="control-btn" @click="toggleFullScreen">
          <FontAwesomeIcon :icon="isFullScreen ? faCompress : faExpand" />
        </button>
      </div>
    </div>
    <div class="video-chatbox">
      <Tabs value="transcription">
        <TabList>
          <Tab value="transcription"
            ><FontAwesomeIcon :icon="faFileText" /><span class="tab-text">Transcription</span></Tab
          >
          <Tab value="summary"
            ><FontAwesomeIcon :icon="faFileText" /><span class="tab-text">Summary</span></Tab
          >
          <Tab value="chat">
            <FontAwesomeIcon :icon="faChain" /><span class="tab-text">Chat</span>
          </Tab>
        </TabList>
        <TabPanels style="flex: 1; height: 0">
          <TabPanel value="transcription">
            <TranscriptionViewer v-if="convertResult" :data="convertResult" />
          </TabPanel>
          <TabPanel value="summary">
            <SummarizationViewer
              v-if="convertResult"
              :segments="convertResult.segments"
              :video_summarization="convertResult.video_summarization"
            />
          </TabPanel>
          <TabPanel value="chat">
            <ChatViewer
              v-if="convertResult"
              :segments="convertResult.segments"
              :video_summarization="convertResult.video_summarization"
            />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { Tab, TabList, TabPanel, TabPanels, Tabs } from 'primevue';
import {
  faBackward,
  faChain,
  faCompress,
  faExpand,
  faFileText,
  faForward,
  faPause,
  faPlay,
  faVolumeUp
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useRoute } from 'vue-router';
import videojs from 'video.js';
import type Player from 'video.js/dist/types/player';
import 'video.js/dist/video-js.css';
import { convertContent, getVideoPaths } from '@/request/meeting'; // ✅ 不再用 getVideoBlob
import TranscriptionViewer from '@/coreComponents/TranscriptionViewer.vue';
import SummarizationViewer from '@/coreComponents/SummarizationViewer.vue';
import ChatViewer from '@/coreComponents/ChatViewer.vue';
import { closeMeetingWindow, openMeetingWindow } from '@/utils/meetingWindowUtils';

// 获取路由参数
const route = useRoute();
const meeting_id = (route.params.meeting_id as string) || '';

// 视频数据结构
interface VideoRecord {
  path: string;
  username: string;
}
interface VideoItem extends VideoRecord {
  url: string;
}
const videos = ref<VideoItem[]>([]);
const players: Player[] = [];
const isPlaying = ref(false);
const currentTime = ref(0);
const totalTime = ref(0);
const globalProgress = ref(0);
const volume = ref(1);
const isFullScreen = ref(false);
const containerRef = ref<HTMLElement | null>(null);

const convertResult = ref();

async function loadVideos() {
  if (!meeting_id) {
    console.error('缺少 meeting_id 参数');
    return;
  }
  try {
    const records: VideoRecord[] = await getVideoPaths(meeting_id);
    console.log(records);

    for (const rec of records) {
      const url = `http://${import.meta.env.VITE_BACKEND_URL}:${import.meta.env.VITE_BACKEND_PORT}/meeting/video?path=${encodeURIComponent(rec.path)}`; // ✅ 使用流接口
      videos.value.push({ path: rec.path, username: rec.username, url });
    }
  } catch (err) {
    console.error('加载视频失败：', err);
  }
}

function updateProgress() {
  const times = players.map(p => p.currentTime());
  currentTime.value = Math.min(Number(...times));
  globalProgress.value = (currentTime.value / totalTime.value) * 100;
}

function togglePlay() {
  if (isPlaying.value) {
    players.forEach(player => {
      player.pause();
    });
  } else {
    players.forEach(player => {
      if (player.readyState() > 0) {
        player.play();
      }
    });
  }
  isPlaying.value = !isPlaying.value;
}

function seekRelative(sec: number) {
  const newTime = Math.max(0, Math.min(totalTime.value, currentTime.value + sec));
  players.forEach(p => p.currentTime(newTime));
  updateProgress();
}

function onProgressClick(e: MouseEvent) {
  const bar = e.currentTarget as HTMLElement;
  const rect = bar.getBoundingClientRect();
  const percent = (e.clientX - rect.left) / rect.width;
  const newTime = percent * totalTime.value;
  players.forEach(p => p.currentTime(newTime));
  updateProgress();
}

function onVolumeChange() {
  players.forEach(p => p.volume(volume.value));
}

function formatTime(sec: number) {
  const m = Math.floor(sec / 60)
    .toString()
    .padStart(2, '0');
  const s = Math.floor(sec % 60)
    .toString()
    .padStart(2, '0');
  return `${m}:${s}`;
}

function toggleFullScreen() {
  if (!containerRef.value) return;
  if (!isFullScreen.value) {
    containerRef.value.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
  isFullScreen.value = !isFullScreen.value;
}

function bindProgressSync() {
  const shortestPlayer = players.reduce((min, p) => {
    const d = p.duration?.() || 0;
    return d > 0 && d <= (min.duration?.() || Infinity) ? p : min;
  }, players[0]);

  if (shortestPlayer) {
    shortestPlayer.on('timeupdate', () => {
      let currentTimeTemp = shortestPlayer.currentTime();
      let totalTimeTemp = shortestPlayer.duration();
      if (!currentTimeTemp || !totalTimeTemp) return;
      currentTime.value = currentTimeTemp;
      totalTime.value = totalTimeTemp;
      globalProgress.value = (currentTime.value / totalTime.value) * 100;
    });
  }
}

onMounted(async () => {
  await openMeetingWindow();
  await loadVideos();
  const content = await convertContent(meeting_id);
  convertResult.value = content;
  await nextTick();
  const videoEls = document.querySelectorAll<HTMLVideoElement>('video.my-video');
  videoEls.forEach((el, index) => {
    const player = videojs(el, {
      controls: false,
      autoplay: false,
      preload: 'auto',
      fluid: true,
      sources: [
        {
          src: videos.value[index].url,
          type: 'video/mp4'
        }
      ]
    });
    players[index] = player;
  });

  bindProgressSync();
});

onBeforeUnmount(async () => {
  players.forEach(p => p.dispose());
  await closeMeetingWindow();
});
</script>

<style scoped lang="scss">
.conference-record {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 10px;

  .video-control {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.6);
    gap: 0.75rem;
    border-radius: 0.5rem;
  }

  .control-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.25rem;
    color: #fff;
    padding: 0.25rem;
    transition: transform 0.2s;
  }

  .control-btn:hover {
    transform: scale(1.1);
  }

  .time-display {
    color: #fff;
    font-size: 0.875rem;
  }

  .progress-bar {
    flex: 1;
    height: 0.5rem;
    background: #444;
    border-radius: 0.25rem;
    cursor: pointer;
    position: relative;
  }

  .progress-filled {
    height: 100%;
    background: #1db954;
    border-radius: 0.25rem 0 0 0.25rem;
  }

  .volume-control {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  .volume-control input {
    width: 4rem;
  }

  .video-panel {
    min-width: 60%;
    height: 100%;
    display: flex;
    gap: 10px;
    flex-direction: column;

    .video-player {
      flex: 1;
      width: 0;
      overflow-y: auto;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;

      .video-item {
        width: 100%;
        height: fit-content;

        .video-content {
          position: relative;

          .video-user {
            font-size: 0.85rem;
            line-height: 0.85rem;
            position: absolute;
            bottom: 35px;
            left: 0.5rem;
            margin: 0 0 5px;
            padding: 0.1rem;
            color: var(--primary-text-color);
            background-color: var(--record-info-background-color);
            border: var(--record-info-border-color);
            border-radius: 0.5rem;
            z-index: 2;
          }

          width: 100%;
          height: min-content;
          background: var(--primary-background-color);
        }
      }
    }

    .video-convert-btn {
      height: 100%;
      width: 100px;

      button {
        all: unset;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .convert {
        background: #4285f4;
        color: #fff;
      }

      .chapter {
        background: #f1f3f4;
      }
    }
  }

  .video-chatbox {
    flex: 1;
    height: 100%;
  }
}
</style>
<style lang="css">
.p-tabs {
  height: 100%;
}
.p-tabpanels {
  height: 0;
  flex: 1;
  width: 100%;
}
.p-tabpanel {
  height: 100%;
}
</style>
