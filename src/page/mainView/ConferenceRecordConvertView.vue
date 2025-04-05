<template>
  <div class="conference-record">
    <div class="video-panel">
      <div class="video-player">
        <video ref="videoElement" controls class="video"></video>
      </div>
      <div class="video-chapter">
        <p style="font-size: 20px; color: #fff;">Chapter</p>
        <div class="video-chapter-panel">
          <Card class="chapter" v-for="chapter in conferenceChapters" :key="chapter.title">
            <template #header>
              <div :style="{ background: `url(${chapter.pic}) no-repeat center center`, backgroundSize: '100% auto' }"
                alt="Chapter Photo" class="chapter-photo"></div>
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
      <Editor class="video-convert-editor" editorStyle="height: calc(100% - 43.35px)" v-model="convertResult">
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
import mpegts from 'mpegts.js';
import { onMounted, ref, useTemplateRef } from 'vue';
import { Card, Divider } from 'primevue';
import Editor from 'primevue/editor';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const videoElementRef = useTemplateRef('videoElement')

const conferenceChapters = ref([
  {
    title: 'Chapter 1',
    startTime: 0,
    pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href
  }, {

    title: 'Chapter 2',
    startTime: 10,
    pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href
  }, {
    title: 'Chapter 3',
    startTime: 20,
    pic: new URL('@/assets/record/record-alt.jpg', import.meta.url).href
  }
])

const convertResult = ref(`The Trump administration justified sweeping tariffs on various countries as “reciprocal,” but the method used to determine them did not actually reflect the tariffs those countries impose on the U.S. Instead, a simplified formula was applied—dividing the U.S. trade deficit with a country by half of its exports to the U.S.—which ignores actual tariff rates and focuses on trade imbalances.

The administration also cited non-tariff barriers like investment restrictions, currency manipulation, and opaque regulations, inflating effective tariff estimates far beyond the official Most-Favored-Nation (MFN) rates set by the WTO. For example, Vietnam’s 9.4% MFN rate was reported as 46% due to non-trade barriers.

Critics argue that these tariffs are arbitrary and aimed at punishing countries with large trade surpluses with the U.S. rather than addressing real trade barriers. Economists also warn that trade deficits are not inherently harmful and that imposing broad tariffs could trigger retaliation, damaging global trade relationships and potentially isolating the U.S. economically.`)

onMounted(() => {
  if (mpegts.getFeatureList().mseLivePlayback) {
    const player = mpegts.createPlayer({
      type: 'mse',  // could also be mpegts, m2ts, flv
      url: 'http://example.com/live/livestream.ts'
    });
    if (videoElementRef.value) {
      player.attachMediaElement(videoElementRef.value);
      player.load();
      player.play();
    }
  }
})
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
      width: 100%;

      video {
        width: 100%;
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