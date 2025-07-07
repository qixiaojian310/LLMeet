// stores/counter.js
import { defineStore } from 'pinia';

interface RecordInfo {
  meetingId: string;
  isRecording: boolean;
}

export const useRecordStore = defineStore('record', {
  state: () => {
    return {
      meetingId: '',
      isRecording: false
    };
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    recordVideo(meetingId: string) {
      this.meetingId = meetingId;
      this.isRecording = true;
    },
    stopRecord() {
      this.isRecording = false;
    }
  }
});
