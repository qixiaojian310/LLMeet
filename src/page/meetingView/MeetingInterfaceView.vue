<template>
  <div class="meeting-view-container">
    <div class="meeting-panel">
      <div class="content">
        <canvas ref="audio" class="audio"></canvas>
        <div class="video">
          <video ref="video" autoplay playsinline></video>
        </div>
      </div>
      <div class="controller">
        <Fieldset>
          <template #legend>
            <div class="chat-header">
              <Avatar :image="mockChatAvater" shape="circle" />
              <span class="font-bold p-2">Amy Elsner</span>
            </div>
          </template>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
            dolore magna
            aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint
            occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
        </Fieldset>
        <Fieldset>
          <template #legend>
            <div class="chat-header">
              <Avatar :image="mockChatAvater" shape="circle" />
              <span class="font-bold p-2">Peter</span>
            </div>
          </template>
          <video controls/>
        </Fieldset>
      </div>
    </div>
    <div class="controls">
      <Button type="button" severity="secondary" @click="toggleVideo">
        <FontAwesomeIcon :icon="controllerState.video ? fas.faVideo : fas.faVideoSlash" size="2x" />
        <p>Video</p>
      </Button>
      <Button type="button" severity="secondary" @click="toggleAudio">
        <FontAwesomeIcon :icon="controllerState.audio ? fas.faMicrophone : fas.faMicrophoneSlash" size="2x" />
        <p>Audio</p>
      </Button>
      <Button type="button" severity="secondary" @click="router.push('/meeting')">
        <FontAwesomeIcon :icon="fas.faHouse" size="2x" />
        <p>Home</p>
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { fas } from '@fortawesome/free-solid-svg-icons';
import { onMounted, onUnmounted, reactive, ref, useTemplateRef } from 'vue';
import { Button, Fieldset, Avatar } from 'primevue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { router } from '@/router';

const video = useTemplateRef('video');
const audioCanvas = useTemplateRef('audio');
const animationId = ref(0);
const audioContext = ref<AudioContext | null>(null)
const controllerState = reactive({
  video: true,
  audio: true,
})

//MOCK
const mockChatAvater = new URL('@/assets/chat/amyelsner.png', import.meta.url).href

let videoStream: MediaStream | null = null;
let audioStream: MediaStream | null = null;

const toggleVideo = async () => {
  controllerState.video = !controllerState.video;

  if (controllerState.video) {
    // 打开摄像头
    if (!videoStream) {
      videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (video.value) {
        video.value.srcObject = videoStream;
      }
    }
    videoStream.getVideoTracks().forEach(track => (track.enabled = true));
  } else {
    // 仅禁用，不销毁
    videoStream?.getVideoTracks().forEach(track => (track.enabled = false));
  }
};

const toggleAudio = async () => {
  controllerState.audio = !controllerState.audio;

  if (controllerState.audio) {
    // 打开麦克风
    audioStream?.getAudioTracks().forEach(track => (track.enabled = true));
    if (audioContext.value?.state === 'suspended') {
      await audioContext.value.resume();
    }
  } else {
    // 仅禁用音轨
    audioStream?.getAudioTracks().forEach(track => (track.enabled = false));
    if (audioContext.value?.state === 'running') {
      await audioContext.value.suspend(); // 暂停音频处理
    }
  }
};

onMounted(async () => {
  try {
    videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (video.value) {
      video.value.srcObject = videoStream;
    }
  } catch (err) {
    console.error("Failed to access camera:", err);
  }
  let analyser: AnalyserNode;
  let microphone: MediaStreamAudioSourceNode;

  try {
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext.value = new (window.AudioContext || (window as any).webkitAudioContext)();
    analyser = audioContext.value.createAnalyser();
    analyser.fftSize = 1024;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    microphone = audioContext.value.createMediaStreamSource(audioStream);
    microphone.connect(analyser);

    const ctx = audioCanvas.value?.getContext('2d');
    if (!ctx || !audioCanvas.value) return;

    const width = audioCanvas.value.width;
    const height = audioCanvas.value.height;

    const draw = () => {
      animationId.value = requestAnimationFrame(draw);

      analyser.getByteFrequencyData(dataArray);

      ctx.fillStyle = 'rgba(39, 38, 38)';
      ctx.fillRect(0, 0, width, height);

      const barWidth = (width / bufferLength) * 2.5;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = dataArray[i];
        ctx.fillStyle = `rgb(${barHeight + 100},50,200)`;
        ctx.fillRect(x, height - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }
    };

    draw();
  } catch (error) {
    console.error("Microphone access failed:", error);
  }
});

onUnmounted(() => {
  videoStream?.getTracks().forEach(track => track.stop());
  audioStream?.getTracks().forEach(track => track.stop());
  cancelAnimationFrame(animationId.value);
});
</script>

<style scoped lang="scss">
.meeting-view-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;

  .meeting-panel {
    display: flex;
    width: 100%;
    flex: 1;
    overflow: hidden;
    gap: 20px;

    .content {
      position: relative;
      flex: 1;
      max-height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #272626;

      .video {
        display: flex;
        justify-content: center;
        flex: 1;
        height: 200px;
        max-width: 100%;

        video {
          width: 100%;
          height: 100%;
        }
      }

      .audio {
        width: 100%;
        height: 50px;
      }
    }

    .controller {
      padding: 20px 20px 0 20px;
      height: 100%;
      width: 300px;
      overflow: auto;
      transition: all 0.3s ease-in-out;
      display: flex;
      flex-direction: column;
      gap: 20px;
      video{
        width: 100%;
      }
    }
  }

  .controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    width: 100%;
    height: 100px;
    background: #272626;

    .p-button {
      display: block;

      p {
        margin: 0;
      }
    }
  }
}
</style>