<template>
  <div class="meeting-view-container">
    <div class="meeting-panel">
      <div class="content">
        <div class="video">
          <!-- 主视频区域 -->
          <div class="main-video">
            <div ref="mainVideoRef" />
          </div>

          <!-- 缩略图区域 -->
          <div class="thumbnails">
            <div
              v-for="item in filteredRemoteVideoTracks"
              :key="item.participantSid"
              class="thumbnail"
              @click="focusTrack(item.track as RemoteTrack)"
            >
              <div :ref="(el) => attachThumbnail(item.track as RemoteTrack, el)" />
            </div>
          </div>
        </div>
      </div>

      <div class="controller">
        <Fieldset legend="LiveKit Room">
          <p>远端视频将自动显示，点击下方按钮可聚焦某一用户视频。</p>
        </Fieldset>
      </div>
    </div>

    <div class="controls">
      <Button type="button" @click="toggleVideo">
        <FontAwesomeIcon
          :icon="controllerState.video ? fas.faVideo : fas.faVideoSlash"
          size="2x"
        />
        <p>Video</p>
      </Button>
      <Button type="button" @click="toggleAudio">
        <FontAwesomeIcon
          :icon="
            controllerState.audio ? fas.faMicrophone : fas.faMicrophoneSlash
          "
          size="2x"
        />
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
} from "livekit-client";
import {
  ref,
  reactive,
  onMounted,
  onBeforeUnmount,
  watch,
  ComponentPublicInstance,
} from "vue";
import { Button, Fieldset } from "primevue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { useMeetingStore } from "@/stores/meetingStore";
import { router } from "@/router";
import { computed } from "vue";


const mainVideoRef = ref<HTMLDivElement | null>(null);
const controllerState = reactive({ video: true, audio: true });
const meetingStore = useMeetingStore();
const token = meetingStore.meetingToken;
const wsUrl = "wss://hkucompcs.xyz:4431";

let room: Room;
interface RemoteVideoTrack {
  participantSid: string;
  track: RemoteTrack;
}
const focusedTrack = ref<RemoteTrack | null>(null);
const remoteVideoTracks = ref<RemoteVideoTrack[]>([]);

const filteredRemoteVideoTracks = computed(() =>
  remoteVideoTracks.value.filter((item) => item.track.sid !== focusedTrack.value?.sid)
);

const attachThumbnail = (
  track: RemoteTrack,
  el: Element | ComponentPublicInstance | null
) => {
  if (!(el instanceof HTMLElement)) return;
  const video = track.attach();
  video.style.width = "100px";
  video.style.height = "60px";
  el.innerHTML = "";
  el.appendChild(video);
};

const focusTrack = (track: RemoteTrack) => {
  if (focusedTrack.value?.sid === track.sid) return; // 不重复赋值
  focusedTrack.value = track;
};

watch(focusedTrack, (newTrack, oldTrack) => {
  if (newTrack?.sid === oldTrack?.sid) return;
  if (oldTrack) oldTrack.detach().forEach((el) => el.remove());
  if (newTrack && mainVideoRef.value) {
    console.log(newTrack);
    
    const element = newTrack.attach();
    element.style.width = "640px";
    element.style.height = "360px";
    mainVideoRef.value.innerHTML = "";
    mainVideoRef.value.appendChild(element);
  }
},{
  flush: 'post'
});

onMounted(async () => {
  room = new Room({
    adaptiveStream: true,
    dynacast: true,
    videoCaptureDefaults: { resolution: VideoPresets.h720.resolution },
  });

  room
    .on(RoomEvent.TrackSubscribed, (track: RemoteTrack, _, participant) => {
      remoteVideoTracks.value.push({
        participantSid: participant.sid,
        track,
      });

      if (!focusedTrack.value) {
        focusedTrack.value = track;
      }
    })
    .on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      track.detach().forEach((el) => el.remove());
    })
    // ✅ 新增对本地 video 的监听（非常重要）
    .on(RoomEvent.LocalTrackPublished, (_, publication) => {
      if (mainVideoRef.value) {
        const videoPub = publication
          .getTrackPublications()
          .find((pub) => pub.kind === Track.Kind.Video);
        if (videoPub?.track && mainVideoRef.value) {
          const element = videoPub.track.attach();
          element.style.width = "640px";
          element.style.height = "360px";
          mainVideoRef.value.appendChild(element);
        }
      }
    })
    .on(RoomEvent.Disconnected, () => {
      console.log("Disconnected from room");
    });

  try {
    await room.connect(wsUrl, token);
    await room.localParticipant.enableCameraAndMicrophone();
  } catch (err) {
    console.error("LiveKit connect failed:", err);
  }
});

onBeforeUnmount(() => {
  room.disconnect();
});

const toggleVideo = () => {
  controllerState.video = !controllerState.video;
  room.localParticipant.getTrackPublications().forEach((pub) => {
    if (pub.kind === Track.Kind.Video && pub.track) {
      pub.track.mediaStreamTrack.enabled = controllerState.video;
    }
  });
};

const toggleAudio = () => {
  controllerState.audio = !controllerState.audio;
  room.localParticipant.getTrackPublications().forEach((pub) => {
    if (pub.kind === Track.Kind.Audio && pub.track) {
      pub.track.mediaStreamTrack.enabled = controllerState.audio;
    }
  });
};

const leaveMeeting = () => {
  room.disconnect();
  meetingStore.clearMeetingInfo();
  router.push({ name: "HomeView" });
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
        flex-direction: column;
        align-items: center;

        .main-video {
          width: 640px;
          height: 360px;
          margin-bottom: 20px;
          background: black;
        }

        .thumbnails {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          justify-content: center;

          .thumbnail {
            cursor: pointer;
            border: 2px solid #ccc;
            padding: 2px;

            &:hover {
              border-color: #fff;
            }

            > div {
              width: 100px;
              height: 60px;
              background: black;
            }
          }
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
