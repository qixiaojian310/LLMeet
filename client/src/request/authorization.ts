import { userStaticStore } from '@/utils/staticStore';
import { requestWrapper } from './requestWrapper';

interface BasicUserInfo {
  username: string;
  password: string;
}

interface RegisterUserInfo extends BasicUserInfo {
  email: string;
}

interface StoreUserInfo {
  username: string;
}

interface UserSetting {
  daily_goal: number;
  reminder_time: string;
}

interface ConvertedUserInfo {
  username: string;
}

export const signin = async (userInfo: BasicUserInfo) => {
  const res = await requestWrapper(
    '/auth/login',
    userInfo,
    {
      method: 'POST'
    },
    false
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);

    await userStaticStore.set('accessToken', body.accessToken);
    const user: StoreUserInfo = {
      username: body.username
    };
    await userStaticStore.set('userInfo', JSON.stringify(user));
    await userStaticStore.save();
    return body;
  } else {
    return res;
  }
};

export const signup = async (userInfo: RegisterUserInfo) => {
  const res = await requestWrapper(
    '/auth/register',
    userInfo,
    {
      method: 'POST'
    },
    false
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    if (body.success) {
      return body;
    }
  } else {
    return res;
  }
};

export const setTimezone = async (timezone: string) => {
  const res = await requestWrapper(
    '/auth/timezone',
    { timezone },
    {
      method: 'POST'
    },
    true
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    console.log('res', body);
    if (body.success) {
      return body;
    }
  } else {
    return res;
  }
};
