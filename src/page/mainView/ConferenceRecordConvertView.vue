<template>
  <div class="conference-record">
    <div class="video-panel">
      <div class="video-player" v-if="videos.length">
        <div
          class="video-item"
          v-for="(video) in videos"
          :key="video.path"
        >
          <p class="video-user">{{ video.userId }}</p>
          <video
            ref="el => videoRefs[index] = el"
            :src="video.url"
            controls
            preload="metadata"
            class="video"
          ></video>
        </div>
      </div>
      <div class="video-chapter">
        <p style="font-size: 20px; color: #fff;">Chapter</p>
        <div class="video-chapter-panel">
          <Card class="chapter" v-for="chapter in conferenceChapters" :key="chapter.title">
            <template #header>
              <div
                :style="{ background: `url(${chapter.pic}) no-repeat center center`, backgroundSize: '100% auto' }"
                alt="Chapter Photo"
                class="chapter-photo"
              ></div>
            </template>
            <template #content>
              <div class="chapter-content">
                <div class="icon">
                  <FontAwesomeIcon :icon="fas.faVideo" />
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
    </div>
    <Divider layout="vertical" />
    <div class="video-convert">
      <Editor
        class="video-convert-editor"
        editorStyle="height: calc(100% - 43.35px)"
        v-model="convertResult"
      >
        <template v-slot:toolbar>
          <span class="ql-formats">
            <button v-tooltip.bottom="'Bold'" class="ql-bold"></button>
            <button v-tooltip.bottom="'Italic'" class="ql-italic"></button>
            <button v-tooltip.bottom="'Underline'" class="ql-underline"></button>
          </span>
        </template>
      </Editor>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { Card, Divider } from 'primevue';
import Editor from 'primevue/editor';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useRoute } from 'vue-router';
import { getVideoPaths, getVideoBlob } from '@/request/meeting';

// 获取 route 中的 meetingId 参数
const route = useRoute();
const meetingId = (route.params.meetingId as string) || '';

// 动态视频列表
interface VideoRecord { path: string; userId: string; }
interface VideoItem extends VideoRecord { url: string; }
const videos = ref<VideoItem[]>([]);
let objectUrls: string[] = [];
const videoRefs: Array<HTMLVideoElement | null> = [];

// 章节数据
const conferenceChapters = ref([
  { title: 'Chapter 1', startTime: 0, pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href },
  { title: 'Chapter 2', startTime: 10, pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href },
  { title: 'Chapter 3', startTime: 20, pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href }
]);

// 转写结果
const convertResult = ref(`...`);

// 加载所有视频
onMounted(async () => {
  if (!meetingId) {
    console.error('缺少 meetingId 参数');
    return;
  }

  try {
    const records: VideoRecord[] = await getVideoPaths(meetingId);
    for (const [index, rec] of records.entries()) {
      const blob = await getVideoBlob(rec.path);
      if (blob instanceof Blob) {
        const url = URL.createObjectURL(blob);
        objectUrls.push(url);
        videos.value.push({ path: rec.path, userId: rec.userId, url });
        // 等 DOM 更新后调用 load()
        await nextTick();
        videoRefs[index]?.load();
      } else {
        console.warn(`获取视频失败: ${rec.path}`, blob);
      }
    }
  } catch (err) {
    console.error('加载视频列表或视频失败：', err);
  }
});

// 组件卸载时释放所有 URL
onBeforeUnmount(() => {
  objectUrls.forEach(u => URL.revokeObjectURL(u));
});
</script>

<style scoped lang="scss">
.conference-record {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 10px;

  .video-panel {
    width: 400px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;

    .video-player {
      flex: 1;
      overflow-y: auto;

      .video-item {
        margin-bottom: 10px;

        .video-user {
          margin: 0 0 5px;
          color: #fff;
        }

        video {
          width: 100%;
          background: #000;
            /* 让原生控件一定显示 */
          appearance: media-play-button !important;
          /* 或者针对 Chrome */
          &::-webkit-media-controls {
            display: block !important;
          }
        }
      }
    }

    .video-chapter {
      flex: 1;
      display: flex;
      flex-direction: column;

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
  }

  .video-convert {
    flex: 1;

    .video-convert-editor {
      height: 100%;
    }
  }
}
</style>
