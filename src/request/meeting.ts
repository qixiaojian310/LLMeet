import { requestWrapper } from './requestWrapper';

export interface MeetingInfo {
  title: string;
  description: string;
  startTime: string;
  endTime: string;
}

export const deleteMeeting = async (meetingId: string) => {
  const res = await requestWrapper(
    '/meeting/delete',
    {
      meetingId: meetingId
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

export const getMeeting = async (meetingId: string) => {
  const res = await requestWrapper(
    '/meeting/get',
    {
      meetingId
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

export const getMeetingToken = async (meetingId: string, username: string) => {
  const res = await requestWrapper(
    '/meeting/token',
    {
      meetingId: meetingId,
      username
    },
    {
      method: 'POST'
    },
    true,
    undefined,
    import.meta.env.VITE_RECORD_BASE_URL
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const startBot = async (meetingId: string) => {
  console.log('startBot', meetingId);

  const res = await requestWrapper(
    '/meeting/start_bot',
    {
      meetingId: meetingId
    },
    {
      method: 'POST'
    },
    true,
    undefined,
    import.meta.env.VITE_RECORD_BASE_URL
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const stopBot = async () => {
  const res = await requestWrapper(
    '/meeting/stop_bot',
    {},
    {
      method: 'POST'
    },
    true,
    undefined,
    import.meta.env.VITE_RECORD_BASE_URL
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getAllMeetingListByUserId = async () => {
  const res = await requestWrapper(
    '/meeting/getAll',
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
    true,
    undefined,
    import.meta.env.VITE_RECORD_BASE_URL
  );
  if (typeof res !== 'number') {
    const body = await res.blob();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};

export const getVideoPaths = async (meetingId: string) => {
  const res = await requestWrapper(
    `/meeting/recordingPath`,
    {
      meetingId
    },
    {
      method: 'POST'
    },
    true,
    undefined,
    import.meta.env.VITE_RECORD_BASE_URL
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    return body;
  } else {
    return res;
  }
};
