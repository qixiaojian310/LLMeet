import {requestWrapper} from './requestWrapper';
import { userStaticStore } from '@/utils/staticStore';

interface BasicUserInfo {
  username: string;
  password: string;
}

interface StoreUserInfo {
  username: string;
  userId: number;
}

interface UserSetting {
  daily_goal: number,
  reminder_time: string,
}

interface ConvertedUserInfo {
  username: string;
  password_hash: string;
}

export const signin = async (
  userInfo: BasicUserInfo
) => {
  const res = await requestWrapper(
    '/api/auth/login',
    userInfo,
    {
      method: 'POST',
    },
    false
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    await userStaticStore.set('accessToken', body.accessToken);
    const user:StoreUserInfo = {
      username: body.username,
      userId: body.userId,
    } 
    await userStaticStore.set('userInfo', JSON.stringify(user));
    await userStaticStore.save();
    return body;
  } else {
    return res;
  }
};

export const signup = async (
  userInfo: BasicUserInfo
) => {
  const res = await requestWrapper(
    '/api/auth/register',
    userInfo,
    {
      method: 'POST',
    },
    false
  );
  if (typeof res !== 'number') {
    const body = await res.json();
    localStorage.setItem('access_token', body);
    localStorage.setItem('userInfo', JSON.stringify(body.user));
    return body;
  } else {
    return res;
  }
};