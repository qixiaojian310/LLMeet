<template>
  <div class="meeting-view-container">
    <div class="header-panel">
      <Button
        severity="secondary"
        style="position: relative"
        @click="
          () => {
            openMeetingInfo = !openMeetingInfo;
          }
        "
      >
        <img height="35px" :src="iconPath" alt="Avatar" />
        <span>Meeting Info</span>
      </Button>
      <div v-if="openMeetingInfo" class="meeting-info">
        <div
          class="meeting-info-item"
          v-for="item in meetingInfo"
          :key="item.title"
        >
          <p class="title">{{ item.title }}</p>
          <p class="value">{{ item.value }}</p>
        </div>
      </div>
    </div>
    <div class="meeting-panel">
      <div class="content">
        <div class="video">
          <!-- 主视频区域 -->
          <div class="main-video">
            <div ref="mainVideoRef" />
            <Button
              class="expander"
              severity="secondary"
              @click="
                () => {
                  openThumbnails = !openThumbnails;
                }
              "
            >
              <FontAwesomeIcon
                v-if="openThumbnails"
                :icon="fas.faChevronRight"
                size="1x"
              />
              <FontAwesomeIcon v-else :icon="fas.faChevronLeft" size="1x" />
            </Button>
          </div>

          <!-- 缩略图区域 -->
          <div :class="`thumbnails ${openThumbnails ? 'open' : 'closed'}`">
            <div
              v-for="item in attachedTracks.filter(
                (item) => item.participantSid !== focusedParticipantSid
              )"
              :key="item.participantSid"
              class="thumbnail"
              @click="focusedParticipantSid = item.participantSid"
            >
              <div :ref="(el) => mountVideo(el, item.participantSid)" />
            </div>
          </div>
        </div>
      </div>
      <!-- 
      <div class="controller">
        <Fieldset legend="LiveKit Room">
          <p>远端视频将自动显示，点击下方按钮可聚焦某一用户视频。</p>
        </Fieldset>
      </div> -->
    </div>

    <div class="controls">
      <Button type="button" severity="secondary" @click="toggleVideo">
        <FontAwesomeIcon
          :icon="controllerState.video ? fas.faVideo : fas.faVideoSlash"
          size="2x"
        />
        <p class="title">Video</p>
      </Button>
      <Button type="button" severity="secondary" @click="toggleAudio">
        <FontAwesomeIcon
          :icon="
            controllerState.audio ? fas.faMicrophone : fas.faMicrophoneSlash
          "
          size="2x"
        />
        <p class="title">Audio</p>
      </Button>
      <Button type="button" severity="secondary" @click="leaveMeeting">
        <FontAwesomeIcon :icon="fas.faSignOutAlt" size="2x" />
        <p class="title">Leave</p>
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
import { Button } from "primevue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { useMeetingStore } from "@/stores/meetingStore";
import { router } from "@/router";
import { computed } from "vue";
import { deleteMeeting, stopBot } from "@/request/meeting";
import { message, notification } from "ant-design-vue";

const mainVideoRef = ref<HTMLDivElement | null>(null);
const controllerState = reactive({ video: true, audio: true });
const meetingStore = useMeetingStore();
const openThumbnails = ref(false);
const openMeetingInfo = ref(false);
const token = meetingStore.meetingToken;
const wsUrl = import.meta.env.VITE_LIVEKIT_WS_URL;
const iconPath = new URL("@/assets/icon/white.png", import.meta.url).href;
let room: Room;

interface AttachedTrack {
  participantSid: string;
  track: RemoteTrack | Track;
  videoElement: HTMLMediaElement;
}
interface MeetingInfoItem {
  title: string;
  value: string;
}
const meetingInfo = computed<MeetingInfoItem[]>(() => {
  return [
    {
      title: "Meeting Name",
      value: meetingStore.meetingName,
    },
    {
      title: "Meeting ID",
      value: meetingStore.meetingId,
    },
    {
      title: "Meeting Description",
      value: meetingStore.description,
    },
    {
      title: "Meeting Start Time",
      value: meetingStore.startTime,
    },
    {
      title: "Meeting End Time",
      value: meetingStore.endTime,
    },
    {
      title: "Meeting Create Time",
      value: meetingStore.createTime,
    },
  ];
});
const attachedTracks = ref<AttachedTrack[]>([]);
const focusedParticipantSid = ref<string | null>(null);

// 存储每个缩略图容器 DOM 的引用
const thumbnailContainers = ref<Record<string, HTMLElement>>({});

// 主视频区域挂载
watch(
  [focusedParticipantSid, attachedTracks],
  () => {
    if (!mainVideoRef.value) return;
    const focused = attachedTracks.value.find(
      (item) => item.participantSid === focusedParticipantSid.value
    );

    mainVideoRef.value.innerHTML = "";
    if (focused) {
      focused.videoElement.style.width = "100%";
      focused.videoElement.style.height = "100%";
      focused.videoElement.style.objectFit = "contain";
      mainVideoRef.value.appendChild(focused.videoElement);
      focused.videoElement.muted = true;
    }
  },
  { flush: "post" }
);

const addOrUpdateAttachedTrack = (
  arr: AttachedTrack[],
  newTrack: AttachedTrack
) => {
  const index = arr.findIndex(
    (item) => item.participantSid === newTrack.participantSid
  );
  if (index !== -1) {
    // 替换旧元素，避免重复
    arr[index] = newTrack;
  } else {
    arr.push(newTrack);
  }
};

// 挂载视频元素到缩略图区域
const mountVideo = (
  el: Element | ComponentPublicInstance | null,
  participantSid: string
) => {
  if (!(el instanceof HTMLElement)) return;
  thumbnailContainers.value[participantSid] = el;

  const trackItem = attachedTracks.value.find(
    (item) => item.participantSid === participantSid
  );
  console.log(trackItem);

  if (trackItem && !el.contains(trackItem.videoElement)) {
    el.innerHTML = "";
    const video = trackItem.videoElement;
    video.style.width = "100%";
    video.style.height = "auto";
    video.style.objectFit = "contain";
    el.appendChild(video);
    video.muted = true;
  }
};

onMounted(async () => {
  room = new Room({
    adaptiveStream: true,
    dynacast: true,
    videoCaptureDefaults: { resolution: VideoPresets.h720.resolution },
    webAudioMix: true,
  });

  room
    .on(RoomEvent.TrackSubscribed, (track: RemoteTrack, _, participant) => {
      console.log("Track subscribed");

      const videoElement = track.attach();
      videoElement.muted = true;
      addOrUpdateAttachedTrack(attachedTracks.value as AttachedTrack[], {
        participantSid: participant.sid,
        track,
        videoElement,
      });

      if (!focusedParticipantSid.value) {
        focusedParticipantSid.value = participant.sid;
      }
    })
    .on(RoomEvent.TrackUnsubscribed, (track: RemoteTrack) => {
      track.detach().forEach((el) => el.remove());

      const index = attachedTracks.value.findIndex(
        (item) => item.track.sid === track.sid
      );
      if (index !== -1) {
        attachedTracks.value.splice(index, 1);
      }

      if (focusedParticipantSid.value === track.sid) {
        focusedParticipantSid.value =
          attachedTracks.value[0]?.participantSid || null;
      }
    })
    .on(RoomEvent.LocalTrackPublished, (_, publication) => {
      const videoPub = publication
        .getTrackPublications()
        .find((pub) => pub.kind === Track.Kind.Video);
      if (videoPub?.track) {
        const videoElement = videoPub.track.attach();

        addOrUpdateAttachedTrack(attachedTracks.value as AttachedTrack[], {
          participantSid: "local",
          track: videoPub.track,
          videoElement,
        });

        if (!focusedParticipantSid.value) {
          focusedParticipantSid.value = "local";
        }
      }
    })
    .on(RoomEvent.AudioPlaybackStatusChanged, () => {
      if (!room.canPlaybackAudio) {
        console.log("Audio playback is disabled");
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
    //撤回会议数据库的添加
    const res = await deleteMeeting(meetingStore.meetingId);
    message.error("Meeting connection failed");
    if (res.success) {
      notification.success({
        message: "Meeting deleted successfully",
        description: "You can now create a new meeting",
      });
    }
  }
});

onBeforeUnmount(async () => {
  room.disconnect();
  await stopBot()
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

  .header-panel {
    display: flex;
    height: 40px;
    background: #27272a;
    position: relative;
    .meeting-info {
      display: flex;
      flex-direction: column;
      position: absolute;
      width: 400px;
      background: #323030;
      top: 130%;
      z-index: 9999;
      box-shadow: 0 0 10px #1a1818;
      border-radius: 10px;
      gap: 15px;
      padding: 10px;
      .meeting-info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        .title {
          color: #ada6a6;
        }
        .value {
          color: #f3f3eb;
        }
        p {
          margin: 0;
        }
      }
    }
  }

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
        align-items: center;
        .main-video {
          flex: 1;
          height: 100%;
          background: rgb(48, 49, 47);
          display: flex;
          justify-content: center;
          align-items: center;
          position: relative;
          .expander {
            position: absolute;
            right: 0;
            top: 50%;
            transform: translate(0, -60%);
            background: #00000088;
          }
        }

        .thumbnails {
          display: flex;
          flex-direction: column;
          gap: 10px;
          justify-content: start;
          overflow: auto;
          background: #00000088;
          transition: width 0.2s ease;
          flex-direction: column;
          height: 100%;
          &.open {
            width: 200px;
          }
          &.closed {
            width: 0;
            visibility: hidden;
          }
          .thumbnail {
            cursor: pointer;
            border: 2px solid #ccc;
            padding: 2px;

            &:hover {
              border-color: #fff;
            }

            > div {
              width: 100%;
              background: black;
              display: flex;
              justify-content: center;
              align-items: center;
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
    height: 80px;
    background: #272626;

    .p-button {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .title {
      margin: 0;
    }
  }
}
</style>
