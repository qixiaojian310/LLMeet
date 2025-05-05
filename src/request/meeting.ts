import { requestWrapper } from "./requestWrapper";

export interface MeetingInfo {
  title: string;
  description: string;
  startTime: string;
  endTime: string;
}

export const createMeeting = async (meetingInfo: MeetingInfo) => {
  const res = await requestWrapper(
    "/meeting/create",
    meetingInfo,
    {
      method: "POST",
    },
    true
  );
  if (typeof res !== "number") {
    const body = await res.json();
    console.log("res", body);
  }else{
    return res;
  }
}