import {useUserStore} from '../stores/userStore';
import {userStaticStore} from '@/utils/staticStore';
let expireCounter = 0;
const MAX_RETRY_TIME = 1;
type methodType = 'GET' | 'POST' | 'PUT' | 'DELETE'
const BASE_URL = 'http://localhost:8080';
// const BASE_URL = 'http://192.168.1.104:8000';

const userStore = useUserStore();

/**
 * This function is used to send a request to the backend, including the user's uid and token, uid is used to identify the user, and token is used to verify the user's identity, uid is stored in the body and accessToken is stored in the header
 * @param requestURL The URL of the request backend, request already have base url so you just need to pass the path like '/api/xxx'
 * @param body The body of the request
 * @returns The response of the backend
 */
export const requestWrapper = async (
  requestURL: string,
  body?: object,
  options?: {
    method?: methodType
    signal?: AbortSignal
  },
): Promise<number | Response> => {
  const { method, signal } = options ?? {};
  const auth = await userStaticStore.get<string>('access_token');
  const requestOptions: any = {
    method: method ?? 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + (auth || ''),
    },
  };
  try {
    const response = await fetch(
      BASE_URL + requestURL,
      {
        ...requestOptions,
        body: body ? JSON.stringify(body) : null,
        signal,
      },
    );
    if (response.ok) {
      return response;
    } else {
      if (expireCounter < MAX_RETRY_TIME) {
        // refresh token
        expireCounter++;
        return requestWrapper(requestURL, body, options);
      } else {
        expireCounter = 0;
        if (response.status === 401) {
          // token expired
          await userStaticStore.delete('access_token');
          userStore.logout();
          return 401;
        }
        return response.status;
      }
    }
  } catch (error: any) {
    console.log('fetch error', error);
    return -1;
  }
};
