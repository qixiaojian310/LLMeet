// stores/counter.js
import { defineStore } from 'pinia'

export const useMeetingStore = defineStore('meeting', {
  state: () => {
    return {
      meetingId: "",
      meetingToken: '',
    }
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    setMeetingInfo(meetingId: string, meetingToken: string) {
      this.meetingId = meetingId;
      this.meetingToken = meetingToken;
    },
    clearMeetingInfo() {
      this.meetingId = "";
      this.meetingToken = '';
    }
  },
})