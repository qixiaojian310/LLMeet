<template>
  <div class="meeting-view-container">
    <div class="meeting-panel">
      <div class="content">
        <div class="video" ref="videoContainer" />
      </div>
      <div class="controller">
        <Fieldset legend="LiveKit Room">
          <p>远端视频将自动显示，点击下方按钮可开关摄像头和麦克风。</p>
        </Fieldset>
      </div>
    </div>
    <div class="controls">
      <Button type="button" @click="toggleVideo">
        <FontAwesomeIcon :icon="controllerState.video ? fas.faVideo : fas.faVideoSlash" size="2x" />
        <p>Video</p>
      </Button>
      <Button type="button" @click="toggleAudio">
        <FontAwesomeIcon :icon="controllerState.audio ? fas.faMicrophone : fas.faMicrophoneSlash" size="2x" />
        <p>Audio</p>
      </Button>
      <Button type="button" @click="leaveMeeting">
        <FontAwesomeIcon :icon="fas.faSignOutAlt" size="2x" />
        <p>Leave Meeting</p>
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Room,
  RoomEvent,
  Track,
  RemoteTrack,
  VideoPresets,
} from 'livekit-client';
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import { Button, Fieldset } from 'primevue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { useMeetingStore } from '@/stores/meetingStore';
import { router } from '@/router';

const videoContainer = ref<HTMLDivElement | null>(null);
const controllerState = reactive({ video: true, audio: true });
const meetingStore = useMeetingStore();
const token = meetingStore.meetingToken; // 请替换为后端生成的token
const wsUrl = 'wss://hkucompcs.xyz:4431'; // 请替换为你的LiveKit服务器地址

let room: Room;

onMounted(async () => {
  room = new Room({
    adaptiveStream: true,
    dynacast: true,
    videoCaptureDefaults: { resolution: VideoPresets.h720.resolution },
  });

  room
    .on(RoomEvent.TrackSubscribed, (track: RemoteTrack) => {
      if (track.kind === Track.Kind.Video && videoContainer.value) {
        const element = track.attach();
        videoContainer.value.appendChild(element);
      }
    })
    .on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      track.detach().forEach((el) => el.remove());
    })
    .on(RoomEvent.Disconnected, () => {
      console.log('Disconnected from room');
    });

  try {
    await room.connect(wsUrl, token);
    await room.localParticipant.enableCameraAndMicrophone();
  } catch (err) {
    console.error('LiveKit connect failed:', err);
  }
});

onBeforeUnmount(() => {
  room.disconnect();
});

// 切换摄像头开关（video）
const toggleVideo = () => {
  controllerState.video = !controllerState.video;

  room.localParticipant.getTrackPublications().forEach((pub) => {
    if (pub.kind === Track.Kind.Video && pub.track) {
      pub.track.mediaStreamTrack.enabled = controllerState.video;
    }
  });
};

// 切换麦克风开关（audio）
const toggleAudio = () => {
  controllerState.audio = !controllerState.audio;

  room.localParticipant.getTrackPublications().forEach((pub) => {
    if (pub.kind === Track.Kind.Audio && pub.track) {
      pub.track.mediaStreamTrack.enabled = controllerState.audio;
    }
  });
};

// 离开会议
const leaveMeeting = () => {
  room.disconnect();
  meetingStore.clearMeetingInfo();
  router.push({ name: 'HomeView' });
};

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
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      background: #272626;

      .video {
        width: 100%;
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;

        video {
          width: 320px;
          height: 180px;
          margin: 5px;
          background: black;
          object-fit: cover;
        }
      }
    }

    .controller {
      width: 300px;
      padding: 20px;
      overflow: auto;
    }
  }

  .controls {
    display: flex;
    justify-content: center;
    gap: 20px;
    height: 100px;
    background: #272626;

    .p-button {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>
