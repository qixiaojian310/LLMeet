// stores/counter.js
import { defineStore } from 'pinia';

interface MeetingInfo {
  meeting_id: string;
  meetingToken: string;
  meetingName: string;
  description: string;
  start_time: string;
  end_time: string;
  create_time: string;
}

export const useMeetingStore = defineStore('meeting', {
  state: () => {
    return {
      meeting_id: '',
      meetingToken: '',
      meetingName: '',
      description: '',
      start_time: '',
      end_time: '',
      create_time: ''
    };
  },
  // 也可以这样定义
  // state: () => ({ count: 0 })
  actions: {
    setMeetingInfo(meetingInfo: MeetingInfo) {
      this.meeting_id = meetingInfo.meeting_id;
      this.meetingToken = meetingInfo.meetingToken;
      this.meetingName = meetingInfo.meetingName;
      this.description = meetingInfo.description;
      this.start_time = meetingInfo.start_time;
      this.end_time = meetingInfo.end_time;
      this.create_time = meetingInfo.create_time;
    },
    clearMeetingInfo() {
      this.meeting_id = '';
      this.meetingToken = '';
      this.meetingName = '';
      this.description = '';
      this.start_time = '';
      this.end_time = '';
      this.create_time = '';
    }
  }
});
