<template>
  <div class="conference-record">
    <div class="video-panel">
      <div class="video-player" v-if="videos.length">
        <div class="video-item" v-for="video in videos" :key="video.path">
          <div class="video-content">
            <p class="video-user">{{ video.userId }}</p>
            <video class="video-js vjs-default-skin my-video" controls></video>
          </div>
        </div>
      </div>
      <div class="video-convert-btn">
        <button @click="()=>{
          showConvert = !showConvert
          showChapter = false;
        }">Convert</button>
        <button @click="()=>{
          showChapter = !showChapter;
          showConvert = false;
        }">Chapter</button>
      </div>
    </div>
    <div class="video-chapter" :class="{ visible: showChapter }">
      <p style="font-size: 20px; color: var(--primary-text-color)">Chapter</p>
      <div class="video-chapter-panel">
        <Card
          class="chapter"
          v-for="chapter in conferenceChapters"
          :key="chapter.title"
        >
          <template #header>
            <div
              :style="{
                background: `url(${chapter.pic}) no-repeat center center`,
                backgroundSize: '100% auto',
              }"
              class="chapter-photo"
            ></div>
          </template>
          <template #content>
            <div class="chapter-content">
              <div class="icon">
                <FontAwesomeIcon :icon="faVideo" />
              </div>
              <div class="text">
                <p class="title">{{ chapter.title }}</p>
                <p class="description">{{ chapter.startTime }}s</p>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
    <div class="video-convert" :class="{ visible: showConvert }">
      <Editor
        class="video-convert-editor"
        editorStyle="height: calc(100% - 43.35px)"
        v-model="convertResult"
      >
        <template v-slot:toolbar>
          <span class="ql-formats">
            <button v-tooltip.bottom="'Bold'" class="ql-bold"></button>
            <button v-tooltip.bottom="'Italic'" class="ql-italic"></button>
            <button
              v-tooltip.bottom="'Underline'"
              class="ql-underline"
            ></button>
          </span>
        </template>
      </Editor>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue";
import { Card } from "primevue";
import Editor from "primevue/editor";
import { faVideo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { useRoute } from "vue-router";
import videojs from "video.js";
import type Player from "video.js/dist/types/player";
import "video.js/dist/video-js.css";
import { getVideoPaths } from "@/request/meeting"; // ✅ 不再用 getVideoBlob

// 获取路由参数
const route = useRoute();
const meetingId = (route.params.meetingId as string) || "";

// 视频数据结构
interface VideoRecord {
  path: string;
  userId: string;
}
interface VideoItem extends VideoRecord {
  url: string;
}
const videos = ref<VideoItem[]>([]);
const players: Player[] = [];
const showConvert = ref(false);
const showChapter = ref(false);
// 示例章节
const conferenceChapters = ref([
  {
    title: "Chapter 1",
    startTime: 0,
    pic: new URL("@/assets/record/record-alt.jpg", import.meta.url).href,
  },
  {
    title: "Chapter 2",
    startTime: 10,
    pic: new URL("@/assets/record/record-alt.jpg", import.meta.url).href,
  },
  {
    title: "Chapter 3",
    startTime: 20,
    pic: new URL("@/assets/record/record-alt.jpg", import.meta.url).href,
  },
]);

const convertResult = ref("...");

async function loadVideos() {
  if (!meetingId) {
    console.error("缺少 meetingId 参数");
    return;
  }
  try {
    const records: VideoRecord[] = await getVideoPaths(meetingId);
    for (const rec of records) {
      const url = `${
        import.meta.env.VITE_RECORD_BASE_URL
      }/meeting/video?path=${encodeURIComponent(rec.path)}`; // ✅ 使用流接口
      videos.value.push({ path: rec.path, userId: rec.userId, url });
    }
  } catch (err) {
    console.error("加载视频失败：", err);
  }
}

onMounted(async () => {
  await loadVideos();
  await nextTick(); // 等待 DOM 渲染后再初始化播放器

  const videoEls =
    document.querySelectorAll<HTMLVideoElement>("video.my-video");
  videoEls.forEach((el, index) => {
    const player = videojs(el, {
      controls: true,
      autoplay: false,
      preload: "auto",
      fluid: true,
      sources: [
        {
          src: videos.value[index].url,
          type: "video/mp4",
        },
      ],
    });
    players[index] = player;
  });
});

onBeforeUnmount(() => {
  players.forEach((p) => p.dispose());
});
</script>

<style scoped lang="scss">
.conference-record {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 10px;

  .video-panel {
    width: 100%;
    height: 100%;
    display: flex;
    gap: 10px;

    .video-player {
      flex: 1;
      width: 0;
      overflow-y: auto;

      .video-item {
        margin-bottom: 10px;
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
          width: 40%;
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

  .video-chapter {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 300px;
    background: linear-gradient(to bottom right, #ffffffee, #f6f0ffcc);
    box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
    transform: translateX(-100%);
    opacity: 0;
    transition: all 0.4s ease;
    display: flex;
    flex-direction: column;
    z-index: 3;
    &.visible {
      transform: translateX(0%);
      opacity: 1;
    }

    .video-chapter-panel {
      height: 100%;
      display: flex;
      overflow-x: auto;
      gap: 10px;
    }

    .chapter {
      height: 100%;
      min-width: 200px;
      max-height: 150px;

      .chapter-photo {
        width: 100%;
        height: 60px;
        border-radius: 10px 10px 0 0;
      }

      .chapter-content {
        display: flex;
        align-items: center;
        gap: 10px;

        p {
          margin: 0;
        }
      }
    }
  }

  .video-convert {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    width: 300px;
    background: linear-gradient(to bottom right, #ffffffee, #f6f0ffcc);
    box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
    transform: translateX(-100%);
    opacity: 0;
    transition: all 0.4s ease;
    z-index: 3;
    &.visible {
      transform: translateX(0%);
      opacity: 1;
    }

    .video-convert-editor {
      height: 100%;
    }
  }
}
</style>
