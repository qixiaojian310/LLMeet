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
      {
        path: "",
        name: "HomeView",
        component: () => import("@/page/mainView/HomeView.vue"),
      },
      {
        path: "meeting-join-form",
        name: "JoinMeeting",
        component: () => import("@/page/mainView/MeetingJoinFormView.vue"),
      },
      {
        path: "meeting-schedule-form",
        name: "CreateMeeting",
        component: () => import("@/page/mainView/MeetingScheduleFormView.vue"),
      },
      {
        path: "conference-records",
        name: "ConferenceRecords",
        component: () => import("@/page/mainView/ConferenceRecordsView.vue"),
      },
      {
        path: "conference-record/:id",
        name: "ConferenceRecord",
        component: () =>
          import("@/page/mainView/ConferenceRecordConvertView.vue"),
      },
    ],
  },
  {
    path: "/register",
    component: RegisterLayout,
    children: [
      { path: "", redirect: "/register/login-form" },
      {
        path: "login-form",
        name: "LoginForm",
        component: () => import("@/page/registerView/LoginFormView.vue"),
      },
      {
        path: "register-form",
        name: "RegisterForm",
        component: () => import("@/page/registerView/RegisterFormView.vue"),
      },
    ],
  },
  {
    path: "/meeting",
    component: MeetingLayout,
    children: [
      {
        path: "",
        name: "MeetingView",
        component: () => import("@/page/meetingView/MeetingInterfaceView.vue"),
      },
    ],
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.name === "/home" && from.name === "LoginForm") {
    next("/home");
  } else {
    next();
  }
});

