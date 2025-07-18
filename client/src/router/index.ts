import { createRouter, RouteRecordRaw, createWebHashHistory } from 'vue-router';

import MainLayout from '@/layout/MainLayout.vue';
import RegisterLayout from '@/layout/RegisterLayout.vue';
import MeetingLayout from '@/layout/MeetingLayout.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/register'
  },
  {
    path: '/home',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'HomeView',
        component: () => import('@/page/mainView/HomeView.vue'),
        meta: {
          title: ''
        }
      },
      {
        path: 'meeting-join-form',
        name: 'JoinMeeting',
        component: () => import('@/page/mainView/MeetingJoinFormView.vue'),
        meta: {
          title: 'Join a meeting'
        }
      },
      {
        path: 'meeting-schedule-form',
        name: 'CreateMeeting',
        component: () => import('@/page/mainView/MeetingScheduleFormView.vue'),
        meta: {
          title: 'Create a meeting'
        }
      },
      {
        path: 'conference-records',
        name: 'ConferenceRecords',
        component: () => import('@/page/recordView/ConferenceRecordsView.vue'),
        meta: {
          title: 'Conference Records'
        }
      },
      {
        path: 'conference-record/:meeting_id',
        name: 'ConferenceRecord',
        component: () => import('@/page/recordView/ConferenceRecordConvertView.vue'),
        meta: {
          title: 'Conference Record'
        }
      },
      {
        path: 'schedule',
        name: 'MeetingSchedule',
        component: () => import('@/page/scheduleView/MeetingSchedule.vue'),
        meta: {
          title: 'Meeting Schedule'
        }
      }
    ]
  },
  {
    path: '/register',
    component: RegisterLayout,
    children: [
      { path: '', redirect: '/register/login-form' },
      {
        path: 'login-form',
        name: 'LoginForm',
        component: () => import('@/page/registerView/LoginFormView.vue'),
        meta: {
          title: 'Login'
        }
      },
      {
        path: 'register-form',
        name: 'RegisterForm',
        component: () => import('@/page/registerView/RegisterFormView.vue'),
        meta: {
          title: 'Register'
        }
      }
    ]
  },
  {
    path: '/meeting',
    component: MeetingLayout,
    children: [
      {
        path: '',
        name: 'MeetingView',
        component: () => import('@/page/meetingView/MeetingInterfaceView.vue'),
        meta: {
          title: 'Meeting'
        }
      }
    ]
  }
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export const noHeaderPages = ['MeetingView'];

router.beforeEach(async (to, from, next) => {
  if (to.name === '/home' && from.name === 'LoginForm') {
    next('/home');
  } else {
    next();
  }
});
