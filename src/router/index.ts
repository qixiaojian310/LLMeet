import { createWebHistory, createRouter } from "vue-router";

import MainLayout from "@/layout/MainLayout.vue";
import RegisterLayout from "@/layout/RegisterLayout.vue";
import MeetingLayout from "@/layout/MeetingLayout.vue";

const routes = [
  {
    path: "/",
    redirect: "/register",
  },
  {
    path: "/home",
    component: MainLayout,
    children: [
      { path: "", name: 'Home View', component: () => import("@/page/mainView/HomeView.vue") },
      { path: 'meeting-join-form', name: 'Join a meeting', component: () => import('@/page/mainView/MeetingJoinFormView.vue')},
      { path: 'meeting-schedule-form', name:'Create a meeting', component: () => import('@/page/mainView/MeetingScheduleFormView.vue')},
      { path: 'conference-records', name:'Conference Records', component: () => import('@/page/mainView/ConferenceRecordsView.vue')},
      { path: 'conference-record/:id', name:'Conference Record', component: () => import('@/page/mainView/ConferenceRecordConvertView.vue')}
    ],
  },
  {
    path: "/register",
    component: RegisterLayout,
    children: [
      { path: "", redirect: "/register/login-form" },
      { path: "login-form", name: 'Login Form', component: () => import("@/page/registerView/LoginFormView.vue")},
      // { path: "/register-form", name: 'Register Form', component: () => import("@/page/RegisterFormView.vue")},
    ]
  },
  {
    path: "/meeting",
    component: MeetingLayout,
    children: [
      { path: "", name: 'Meeting View', component: () => import("@/page/meetingView/MeetingInterfaceView.vue") },
    ],
  }
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});


