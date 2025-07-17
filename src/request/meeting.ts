import { requestWrapper } from './requestWrapper';

export interface MeetingInfo {
  title: string;
  description: string;
  start_time: string;
  end_time: string;
}

export const joinMeeting = async (meeting_id: string) => {
  const res = await requestWrapper(
    `/meeting/join`,
    {
      meeting_id
    },
    {
      method: 'POST'
    },
    true,
    undefined
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const deleteMeeting = async (meeting_id: string) => {
  const res = await requestWrapper(
    '/meeting/delete',
    {
      meeting_id: meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const createMeeting = async (meetingInfo: MeetingInfo) => {
  const res = await requestWrapper(
    '/meeting/create',
    meetingInfo,
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getMeeting = async (meeting_id: string) => {
  const res = await requestWrapper(
    '/meeting/get',
    {
      meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getMeetingToken = async (meeting_id: string, username: string) => {
  const res = await requestWrapper(
    '/meeting/token',
    {
      meeting_id: meeting_id,
      username
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const startBot = async (meeting_id: string) => {
  console.log('startBot', meeting_id);

  const res = await requestWrapper(
    '/meeting/start_bot',
    {
      meeting_id: meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const stopBot = async (meeting_id: string) => {
  const res = await requestWrapper(
    '/meeting/stop_bot',
    {
      meeting_id: meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getAllMeetingListByUsername = async () => {
  const res = await requestWrapper(
    '/meeting/get_all',
    undefined,
    {
      method: 'GET'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getAllMeetingListWithRecordByUsername = async () => {
  const res = await requestWrapper(
    '/meeting/get_all_with_records',
    undefined,
    {
      method: 'GET'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getVideoBlob = async (path: string) => {
  const res = await requestWrapper(
    `/meeting/video`,
    {
      path
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.blob();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getVideoPaths = async (meeting_id: string) => {
  const res = await requestWrapper(
    `/meeting/recordingPath`,
    {
      meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const convertContent = async (meeting_id: string) => {
  const res = await requestWrapper(
    `/meeting/convert_content`,
    {
      meeting_id
    },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getSummary = async (segments: any[], video_summarization: string) => {
  const res = await requestWrapper(
    `/meeting/v1/chat/summarization`,
    {
      segments,
      video_summarization
    },
    {
      method: 'POST'
    },
    true
  );
  return res;
};

export async function getChatStream(messages: any, segments: any, video_summarization: string) {
  const res = await requestWrapper(
    `/meeting/v1/chat/completions`,
    {
      messages,
      segments,
      video_summarization
    },
    {
      method: 'POST'
    },
    true
  );
  return res;
}
