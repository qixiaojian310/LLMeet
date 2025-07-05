// stores/counter.js
import { defineStore } from 'pinia';

interface MeetingInfo {
  meetingId: string;
  meetingToken: string;
  meetingName: string;
  description: string;
  startTime: string;
  endTime: string;
  createTime: string;
}

export const useMeetingStore = defineStore('meeting', {
  state: () => {
    return {
      meetingId: '',
      meetingToken: '',
      meetingName: '',
      description: '',
      startTime: '',
      endTime: '',
      createTime: ''
    };
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    setMeetingInfo(meetingInfo: MeetingInfo) {
      this.meetingId = meetingInfo.meetingId;
      this.meetingToken = meetingInfo.meetingToken;
      this.meetingName = meetingInfo.meetingName;
      this.description = meetingInfo.description;
      this.startTime = meetingInfo.startTime;
      this.endTime = meetingInfo.endTime;
      this.createTime = meetingInfo.createTime;
    },
    clearMeetingInfo() {
      this.meetingId = '';
      this.meetingToken = '';
      this.meetingName = '';
      this.description = '';
      this.startTime = '';
      this.endTime = '';
      this.createTime = '';
    }
  }
});
