import { livekitRequestWrapper } from "./livekitRequestWrapper";
import { requestWrapper } from "./requestWrapper";

export interface MeetingInfo {
  title: string;
  description: string;
  startTime: string;
  endTime: string;
}

export const deleteMeeting = async (meetingId: string) => {
  const res = await requestWrapper(
    "/meeting/delete",
    {
      meetingId: meetingId,
    },
    {
      method: "POST",
    },
    true
  );
  if (typeof res !== "number") {
    const body = await res.json();
    console.log("res", body);
    return body;
  } else {
    return res;
  }
};

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
    return body;
  } else {
    return res;
  }
};

export const getMeetingToken = async (meetingId: string, username: string) => {
  const res = await livekitRequestWrapper(
    "/meeting/token",
    {
      meetingId: meetingId,
      username,
    },
    {
      method: "POST",
    },
    true
  );
  if (typeof res !== "number") {
    const body = await res.json();
    console.log("res", body);
    return body;
  } else {
    return res;
  }
};
