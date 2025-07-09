// stores/counter.js
import { defineStore } from 'pinia';

interface RecordInfo {
  meeting_id: string;
  isRecording: boolean;
}

export const useRecordStore = defineStore('record', {
  state: () => {
    return {
      meeting_id: '',
      isRecording: false
    };
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    recordVideo(meeting_id: string) {
      this.meeting_id = meeting_id;
      this.isRecording = true;
    },
    stopRecord() {
      this.isRecording = false;
    }
  }
});
